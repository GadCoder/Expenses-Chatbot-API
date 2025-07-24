import logging
from functools import lru_cache

from openai import OpenAI

from src.core.config import settings
from src.services.llm.base import BaseLLMService
from services.llm.tools_registry import get_tools

logger = logging.getLogger(__name__)


class OpenAIService(BaseLLMService):
    def __init__(self):
        logger.info("Initializing OpenAI Service...")
        self.client: OpenAI = OpenAI(api_key=settings.LLM_API_KEY)

    def get_function_call(self, prompt: str) -> tuple | None:
        logger.info(f"Sending prompt to OpenAI: {prompt}")
        response = self.client.responses.create(
            model=settings.LLM_MODEL,
            input=[{"role": "user", "content": prompt}],
            tools=get_tools(),
        )
        function_call = response.output[0]
        if not function_call:
            logger.warning("No function call returned from OpenAI")
            return None
        logger.info(f"Received function call from OpenAI: {function_call.name}")
        return (function_call.name, function_call.arguments)


@lru_cache
def get_openai_service() -> OpenAIService:
    return OpenAIService()
