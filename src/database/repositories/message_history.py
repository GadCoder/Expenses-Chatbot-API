import logging

from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.models.message_history import MessageHistory
from database.schemas.message_history import MessageHistoryCreate

logger = logging.getLogger(__name__)


def create_message_history(
    db: Session, message_history: MessageHistoryCreate
) -> MessageHistory:
    logger.debug(f"Creating message history for user_id: {message_history.user_id}")
    db_message_history = MessageHistory(**message_history.model_dump())
    db.add(db_message_history)
    db.commit()
    db.refresh(db_message_history)
    return db_message_history


def get_message_history_by_user_id(db: Session, user_id: int) -> list[MessageHistory]:
    logger.debug(f"Getting message history for user_id: {user_id}")
    messages = (
        db.query(MessageHistory)
        .filter(MessageHistory.user_id == user_id, MessageHistory.sender_type == "USER")
        .order_by(desc(MessageHistory.created_at))
        .limit(10)
        .all()
    )
    return list(reversed(messages))
