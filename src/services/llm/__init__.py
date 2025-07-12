from src.core.config import settings
from src.services.llm.base import BaseLLMService
from services.llm.providers.gemini import get_gemini_service
from services.llm.providers.openai import get_openai_service


def get_llm_service() -> BaseLLMService:
    if settings.LLM_PROVIDER == "gemini":
        return get_gemini_service()
    if settings.LLM_PROVIDER == "openai":
        return get_openai_service()
    else:
        raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
