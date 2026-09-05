from .agent import run_agent
from .config import GROQ_MODEL, GEMINI_MODEL
from .llm import get_llm


SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You have tools to:
- Explore the filesystem: list files, view directory trees, get file metadata (size, type, modified time), and check the current working directory.
- Search & navigate: search files by name/content and search source code (`search_code`) with line numbers.
- Manage & edit files: read files, write files, modify specific sections of files with diffs (`modify_file`), create directories, move/rename files, and delete files.
- Execute shell commands: run terminal commands when needed.

Important Rules:
- If a tool output indicates that the user declined or rejected an action (e.g. user declined a shell command, file deletion, or code modification), you MUST IMMEDIATELY STOP attempting that action. Never re-prompt, retry, or call the tool again with variations of the same command. Acknowledge that the action was cancelled and ask the user how they would like to proceed.
- Use your tools to complete the user's task, then briefly summarize what you did.
- The working directory is the folder the user launched you from."""


def choose_provider() -> str:
    """Prompt the user to select their desired LLM provider at startup."""
    print("=" * 45)
    print(" Select LLM Provider:")
    print(f" [1] Groq ({GROQ_MODEL})")
    print(f" [2] Gemini ({GEMINI_MODEL})")
    print("=" * 45)

    choice = input("Enter choice [1/2] (default: 1): ").strip().lower()

    if choice in ("2", "gemini"):
        return "gemini"
    return "groq"


def main():
    provider = choose_provider()

    try:
        llm = get_llm(provider)
        print(f"\nLoaded provider: {provider.upper()} ({llm.model})")
    except Exception as error:
        print(f"\nFailed to initialize {provider}: {error}")
        return

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

        reply = run_agent(messages, llm=llm)

        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    main()