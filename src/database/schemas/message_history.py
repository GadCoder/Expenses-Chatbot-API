from datetime import datetime
from pydantic import BaseModel, Field


class MessageHistoryBase(BaseModel):
    user_id: int
    message: str
    sender_type: str
    categories: str | None = Field(default=None)
    delta_time: int | None = Field(default=None)


class MessageHistoryCreate(MessageHistoryBase):
    pass


class MessageHistory(MessageHistoryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
