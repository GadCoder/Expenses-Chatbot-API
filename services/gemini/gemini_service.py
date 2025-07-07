from google import genai
from google.genai import types

from core.config import settings
from gemini_tools import register_expense

client = genai.Client(api_key=settings.gemini_api_key)
tools = types.Tool(function_declarations=[register_expense])
config = types.GenerateContentConfig(tools=[tools])
