import copy
import json
import uuid
from google import genai
from google.genai import types

from .base import LLM
from ..config import GEMINI_API_KEY, GEMINI_MODEL
from ..tools.schemas import TOOL_SCHEMAS


class FunctionCallWrapper:
    """Wrapper to provide an OpenAI-compatible function object."""

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments if isinstance(arguments, str) else json.dumps(arguments)


class ToolCallWrapper:
    """Wrapper to provide an OpenAI-compatible tool call object."""

    def __init__(self, id, name, arguments):
        self.id = id or f"call_{uuid.uuid4().hex[:8]}"
        self.type = "function"
        self.function = FunctionCallWrapper(name, arguments)


class MessageWrapper:
    """Wrapper to provide an OpenAI-compatible message object."""

    def __init__(self, role, content=None, tool_calls=None, gemini_content=None):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls or []
        self.gemini_content = gemini_content


class ChoiceWrapper:
    """Wrapper to provide an OpenAI-compatible choice object."""

    def __init__(self, message):
        self.message = message


class ResponseWrapper:
    """Wrapper to provide an OpenAI-compatible response object."""

    def __init__(self, choices):
        self.choices = choices


class GeminiLLM(LLM):
    """Gemini LLM implementation using the google-genai SDK."""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=120000),
        )
        self.model = GEMINI_MODEL

    def _sanitize_schema(self, schema):
        """Recursively strip fields unsupported by Gemini function declarations (e.g. additionalProperties)."""
        if not isinstance(schema, dict):
            return schema

        cleaned = copy.deepcopy(schema)
        cleaned.pop("additionalProperties", None)
        cleaned.pop("additional_properties", None)

        if "properties" in cleaned and isinstance(cleaned["properties"], dict):
            for prop_name, prop_val in cleaned["properties"].items():
                cleaned["properties"][prop_name] = self._sanitize_schema(prop_val)

        return cleaned

    def _convert_tools(self, tools=None):
        """Convert OpenAI-style tool schemas into Gemini FunctionDeclaration and Tool objects."""
        raw_tools = tools if tools is not None else TOOL_SCHEMAS
        if not raw_tools:
            return None

        declarations = []
        for tool in raw_tools:
            function = tool.get("function", tool)
            params = self._sanitize_schema(function.get("parameters"))

            declarations.append(
                types.FunctionDeclaration(
                    name=function["name"],
                    description=function.get("description", ""),
                    parameters=params,
                )
            )

        return [types.Tool(function_declarations=declarations)]

    def _format_messages_for_gemini(self, messages):
        """Convert conversational messages into Gemini system instruction and Content items."""
        system_instructions = []
        contents = []
        call_id_to_name = {}

        i = 0
        while i < len(messages):
            msg = messages[i]
            role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)

            if role == "system":
                content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
                if content:
                    system_instructions.append(str(content))
                i += 1

            elif role == "user":
                content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=str(content))],
                    )
                )
                i += 1

            elif role == "assistant":
                # Preserve existing Gemini Content object (including thought signatures) if available
                gemini_content = getattr(msg, "gemini_content", None)
                if gemini_content:
                    contents.append(gemini_content)
                else:
                    parts = []
                    content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
                    if content:
                        parts.append(types.Part.from_text(text=str(content)))

                    tool_calls = getattr(msg, "tool_calls", None) or (msg.get("tool_calls") if isinstance(msg, dict) else None)
                    if tool_calls:
                        for tc in tool_calls:
                            if hasattr(tc, "function"):
                                fn_name = tc.function.name
                                fn_args = tc.function.arguments
                                tc_id = getattr(tc, "id", None)
                            else:
                                fn_name = tc.get("function", {}).get("name")
                                fn_args = tc.get("function", {}).get("arguments")
                                tc_id = tc.get("id")

                            if tc_id and fn_name:
                                call_id_to_name[tc_id] = fn_name

                            if isinstance(fn_args, str):
                                try:
                                    fn_args = json.loads(fn_args)
                                except Exception:
                                    fn_args = {}

                            parts.append(types.Part.from_function_call(name=fn_name, args=fn_args or {}))

                    if parts:
                        contents.append(types.Content(role="model", parts=parts))

                # Track call_id -> name
                tool_calls = getattr(msg, "tool_calls", None) or (msg.get("tool_calls") if isinstance(msg, dict) else None)
                if tool_calls:
                    for tc in tool_calls:
                        tc_id = getattr(tc, "id", None) or (tc.get("id") if isinstance(tc, dict) else None)
                        tc_name = getattr(getattr(tc, "function", None), "name", None) or (tc.get("function", {}).get("name") if isinstance(tc, dict) else None)
                        if tc_id and tc_name:
                            call_id_to_name[tc_id] = tc_name
                i += 1

            elif role == "tool":
                # In Gemini, group consecutive tool responses into a single Content(role="user", parts=...)
                tool_parts = []
                while i < len(messages):
                    curr = messages[i]
                    curr_role = curr.get("role") if isinstance(curr, dict) else getattr(curr, "role", None)
                    if curr_role != "tool":
                        break

                    tc_id = curr.get("tool_call_id") if isinstance(curr, dict) else getattr(curr, "tool_call_id", None)
                    name = curr.get("name") if isinstance(curr, dict) else getattr(curr, "name", None)
                    if not name and tc_id in call_id_to_name:
                        name = call_id_to_name[tc_id]

                    output = curr.get("content") if isinstance(curr, dict) else getattr(curr, "content", "")
                    tool_parts.append(
                        types.Part.from_function_response(
                            name=name or "tool",
                            response={"output": str(output)},
                        )
                    )
                    i += 1

                if tool_parts:
                    contents.append(types.Content(role="user", parts=tool_parts))

            else:
                i += 1

        system_instruction = "\n\n".join(system_instructions) if system_instructions else None
        return system_instruction, contents

    def generate(self, messages, tools=None):
        """Send messages and tools to Gemini, returning a response compatible with the agent loop."""
        system_instruction, contents = self._format_messages_for_gemini(messages)
        gemini_tools = self._convert_tools(tools)

        config_kwargs = {}
        if gemini_tools:
            config_kwargs["tools"] = gemini_tools
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0] if response.candidates else None
        if not candidate or not candidate.content:
            return ResponseWrapper([ChoiceWrapper(MessageWrapper(role="assistant", content=""))])

        tool_calls = []
        if response.function_calls:
            for fc in response.function_calls:
                call_id = fc.id or f"call_{uuid.uuid4().hex[:8]}"
                args = dict(fc.args) if fc.args else {}
                tool_calls.append(
                    ToolCallWrapper(
                        id=call_id,
                        name=fc.name,
                        arguments=json.dumps(args),
                    )
                )

        # Extract textual content safely from content parts
        text_content = None
        if not tool_calls and candidate.content.parts:
            text_parts = [part.text for part in candidate.content.parts if getattr(part, "text", None)]
            if text_parts:
                text_content = "".join(text_parts)

        message = MessageWrapper(
            role="assistant",
            content=text_content,
            tool_calls=tool_calls,
            gemini_content=candidate.content,
        )

        return ResponseWrapper([ChoiceWrapper(message)])