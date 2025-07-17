from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from database.database import Base


class MessageHistory(Base):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    sender_type = Column(String)
    categories = Column(String, nullable=True)
    delta_time = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User")
