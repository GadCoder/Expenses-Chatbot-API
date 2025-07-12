from src.core.config import settings
from src.services.llm.base import BaseLLMService
from src.services.llm.providers.gemini.gemini_service import get_gemini_service


def get_llm_service() -> BaseLLMService:
    if settings.LLM_PROVIDER == "gemini":
        return get_gemini_service()
    # Add other providers here
    else:
        raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
