from .agent import run_agent


SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from."""


def main():
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    print("Mini agent ready. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")

        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        reply = run_agent(messages)

        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    main()