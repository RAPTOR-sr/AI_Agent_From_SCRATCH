import json

from .config import client, MODEL
from .tools import TOOLS
from .tools.schemas import TOOL_SCHEMAS


def run_tool(tool_call):
    """Execute a tool requested by the model."""

    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    #print(f"Tool: {name} ({args})")

    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"


def run_agent(messages):
    """Run the agent loop until the model returns a final response."""

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message
        messages.append(message)

        # Model has finished and doesn't need a tool.
        if not message.tool_calls:
            return message.content

        # Execute every tool requested by the model.
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )