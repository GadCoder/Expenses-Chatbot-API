from sqlalchemy.orm import Session

from .enrich_prompt import enrich_prompt
from ..tool_registry import TOOL_REGISTRY
from ..gemini.gemini_service import GeminiService

from .enrich_answer import enrich_answer
from database.repositories.user import get_user_by_chat_id


def process_message(
    db: Session,
    chat_id: str,
    message: str,
    gemini: GeminiService,
):
    user = get_user_by_chat_id(db=db, chat_id=chat_id)
    enriched_prompt = enrich_prompt(db=db, message=message, user_id=user.id)  # type: ignore
    function_call = gemini.get_function_call(prompt=enriched_prompt)
    if not function_call:
        return None
    function_name, function_args = function_call  # type: ignore
    print(f"Function name: {function_name} Args: {function_args}")
    if function_name not in TOOL_REGISTRY:
        return None
    function_to_call = TOOL_REGISTRY[function_name]
    function_args["db"] = db
    function_args["user"] = user
    result = function_to_call(**function_args)
    enriched_answer = enrich_answer(function_name=function_name, result=result)
    return enriched_answer
