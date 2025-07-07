from typing import List
from pydantic import BaseModel

from .expense import ExpenseRead
from .expense_category import ExpenseCategoryRead


class UserBase(BaseModel):
    chat_id: str
    name: str
    bot_name: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    expenses: List[ExpenseRead] = []
    categories: List[ExpenseCategoryRead] = []

    class Config:
        orm_mode = True
