from .agent import run_agent
from .config import GROQ_MODEL, GEMINI_MODEL
from .llm import get_llm


SYSTEM_PROMPT = """You are Terminal agent. Use tools to manage files, search, and run shell commands. Summarize actions when finished. Base path: current working directory.

Important Rules:
user declined or rejected an action then IMMEDIATELY STOP attempting that action"""


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