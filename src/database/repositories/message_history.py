from sqlalchemy.orm import Session

from database.models.message_history import MessageHistory
from database.schemas.message_history import MessageHistoryCreate


def create_message_history(db: Session, message_history: MessageHistoryCreate) -> MessageHistory:
    db_message_history = MessageHistory(**message_history.model_dump())
    db.add(db_message_history)
    db.commit()
    db.refresh(db_message_history)
    return db_message_history


def get_message_history_by_user_id(db: Session, user_id: int) -> list[MessageHistory]:
    return db.query(MessageHistory).filter(MessageHistory.user_id == user_id).order_by(MessageHistory.created_at).all()
