import logging
from functools import lru_cache

from google.genai import types, Client

from src.core.config import settings
from src.services.llm.base import BaseLLMService
from services.llm.tools_registry import get_tools

logger = logging.getLogger(__name__)


class GeminiService(BaseLLMService):
    def __init__(self):
        logger.info("Initializing Gemini Service...")
        self.client: Client = Client(api_key=settings.LLM_API_KEY)
        tools = types.Tool(function_declarations=get_tools())
        self.config = types.GenerateContentConfig(tools=[tools])

    def get_function_call(self, prompt: str) -> tuple | None:
        logger.info(f"Sending prompt to Gemini: {prompt}")
        response = self.client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=prompt,
            config=self.config,
        )
        function_call = response.candidates[0].content.parts[0].function_call
        if not function_call:
            logger.warning("No function call returned from Gemini")
            return None
        logger.info(f"Received function call from Gemini: {function_call.name}")
        return (function_call.name, function_call.args)


@lru_cache
def get_gemini_service() -> GeminiService:
    return GeminiService()
