from google.genai import types, Client

from core.config import settings
from services.gemini.gemini_tools_registry import get_tools


class GeminiService:
    def __init__(self):
        print("Initializing Gemini Service...")
        self.client: Client = Client(api_key=settings.gemini_api_key)
        tools = types.Tool(function_declarations=get_tools())  # type: ignore
        self.config = types.GenerateContentConfig(tools=[tools])  # type: ignore

    def get_function_call(self, prompt: str) -> tuple | None:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=prompt,
            config=self.config,
        )
        function_call = response.candidates[0].content.parts[0].function_call  # type: ignore
        if not function_call:
            return None
        return (function_call.name, function_call.args)


gemini_service = GeminiService()


def get_gemini_service() -> GeminiService:
    return gemini_service
