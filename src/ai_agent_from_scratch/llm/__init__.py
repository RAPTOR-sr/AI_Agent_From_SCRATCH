from ..config import LLM_PROVIDER
from .base import LLM
from .gemini import GeminiLLM
from .groq import GroqLLM


def get_llm(provider: str | None = None) -> LLM:
    """Factory function to get the configured LLM instance."""
    provider_name = (provider or LLM_PROVIDER or "groq").strip().lower()

    if provider_name == "groq":
        return GroqLLM()
    elif provider_name == "gemini":
        return GeminiLLM()
    else:
        raise ValueError(
            f"Unsupported LLM provider '{provider_name}'. Supported providers: 'groq', 'gemini'."
        )


__all__ = ["LLM", "GroqLLM", "GeminiLLM", "get_llm"]

