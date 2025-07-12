import logging
from typing import Callable, Dict, Optional, Tuple

from sqlalchemy.orm import Session

from .enrich_prompt import enrich_prompt
from .enrich_answer import enrich_answer
from ..tool_registry import TOOL_REGISTRY
from ..gemini.gemini_service import GeminiService
from database.repositories.user import get_user_by_chat_id
from database.schemas.message_history import MessageHistoryCreate
from database.repositories.message_history import (
    create_message_history,
    get_message_history_by_user_id,
)


logger = logging.getLogger(__name__)


def process_message(
    db: Session,
    chat_id: str,
    message: str,
    gemini: GeminiService,
):
    logger.info(f"Processing message from chat_id: {chat_id}")
    user = get_user_by_chat_id(db=db, chat_id=chat_id)

    create_message_history(
        db=db,
        message_history=MessageHistoryCreate(
            user_id=user.id,
            message=message,
            sender_type="USER",  # type: ignore
        ),
    )

    message_history = get_message_history_by_user_id(db=db, user_id=user.id)  # type: ignore
    enriched_prompt = enrich_prompt(
        db=db, message=message, user_id=user.id, message_history=message_history
    )  # type: ignore

    result = get_function_to_call(gemini=gemini, prompt=enriched_prompt)
    if result is None:
        logger.warning("Could not determine function to call")
        return None

    function_name, function_to_call, function_args = result
    function_args.update({"db": db, "user": user})  # type: ignore

    logger.info(f"Calling function: {function_name}")
    answer = function_to_call(**function_args)  # type: ignore

    enriched_answer = enrich_answer(function_name=function_name, answer=answer)
    create_message_history(
        db=db,
        message_history=MessageHistoryCreate(
            user_id=user.id,
            message=enriched_answer,
            sender_type="BOT",  # type: ignore
        ),
    )

    logger.info(f"Sending answer to chat_id: {chat_id}")
    return enriched_answer


def get_function_to_call(
    gemini: GeminiService, prompt: str
) -> Optional[Tuple[str, Callable, Dict]]:
    function_call = gemini.get_function_call(prompt=prompt)
    if not function_call:
        return None

    function_name, function_args = function_call
    function_to_call = TOOL_REGISTRY.get(function_name)
    if not function_to_call:
        return None

    return function_name, function_to_call, function_args
