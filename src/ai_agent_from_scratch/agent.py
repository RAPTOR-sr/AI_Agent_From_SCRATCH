import json

from .llm import get_llm
from .tools import TOOLS
from .tools.schemas import TOOL_SCHEMAS


def run_tool(tool_call):
    """Execute a tool requested by the model."""

    name = tool_call.function.name
    args = tool_call.function.arguments
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except Exception:
            args = {}

    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"


def run_agent(messages, llm=None, max_iterations=15):
    """Run the agent loop until the model returns a final response."""
    if llm is None:
        llm = get_llm()

    iterations = 0
    while iterations < max_iterations:
        iterations += 1
        response = llm.generate(
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message
        messages.append(message)

        # Model has finished and doesn't need a tool.
        if not message.tool_calls:
            return message.content or ""

        # Execute every tool requested by the model.
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": result,
                }
            )

    return "Agent reached maximum tool execution iterations for this request."