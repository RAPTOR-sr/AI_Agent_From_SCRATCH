from .agent import run_agent


SYSTEM_PROMPT = """Terminal agent. Use tools to manage files, search, and run shell commands. 
Summarize actions when finished. then briefly summarize what you did. 
Base path: current working directory.
"""


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