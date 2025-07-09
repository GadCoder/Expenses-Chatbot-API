from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from ..database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String)
    name = Column(String, nullable=True)
    bot_name = Column(String, nullable=True)

    expenses = relationship(
        "Expense", back_populates="user", cascade="all, delete-orphan"
    )
    categories = relationship(
        "ExpenseCategory", back_populates="user", cascade="all, delete-orphan"
    )
