import json
from groq import Groq

from .base import LLM
from ..config import GROQ_API_KEY, GROQ_MODEL


class GroqLLM(LLM):

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the environment.")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def _format_messages(self, messages):
        """Ensure all messages are plain dicts or OpenAI compatible objects."""
        formatted = []
        for msg in messages:
            if isinstance(msg, dict):
                formatted.append(msg)
            elif hasattr(msg, "role"):
                item = {"role": msg.role}
                if getattr(msg, "content", None) is not None:
                    item["content"] = msg.content
                tool_calls = getattr(msg, "tool_calls", None)
                if tool_calls:
                    item["tool_calls"] = [
                        {
                            "id": getattr(tc, "id", None),
                            "type": "function",
                            "function": {
                                "name": getattr(getattr(tc, "function", None), "name", None),
                                "arguments": getattr(getattr(tc, "function", None), "arguments", "{}"),
                            },
                        }
                        for tc in tool_calls
                    ]
                formatted.append(item)
            else:
                formatted.append(msg)
        return formatted

    def generate(self, messages, tools=None):
        payload_messages = self._format_messages(messages)
        kwargs = {
            "model": self.model,
            "messages": payload_messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)
        return response