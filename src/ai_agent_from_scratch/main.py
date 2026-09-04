from .agent import run_agent


SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You have tools to:
- Explore the filesystem: list files, view directory trees, get file metadata (size, type, modified time), and check the current working directory.
- Search & navigate: search files by name/content and search source code (`search_code`) with line numbers.
- Manage & edit files: read files, write files, modify specific sections of files with diffs (`modify_file`), create directories, move/rename files, and delete files.
- Execute shell commands: run terminal commands when needed.

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