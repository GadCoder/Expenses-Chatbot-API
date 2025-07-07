from typing import List
from pydantic import BaseModel, Field

from .expense import ExpenseRead
from .expense_category import ExpenseCategoryRead


class UserBase(BaseModel):
    chat_id: str
    name: str | None = Field(default=None)
    bot_name: str | None = Field(default=None)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    chat_id: str
    expenses: List[ExpenseRead] = []
    categories: List[ExpenseCategoryRead] = []

    class Config:
        orm_mode = True
