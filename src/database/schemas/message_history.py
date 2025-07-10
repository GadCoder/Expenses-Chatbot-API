from datetime import datetime
from pydantic import BaseModel


class MessageHistoryBase(BaseModel):
    message: str
    sender_type: str


class MessageHistoryCreate(MessageHistoryBase):
    user_id: int


class MessageHistory(MessageHistoryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
