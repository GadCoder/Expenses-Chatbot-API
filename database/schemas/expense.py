from datetime import datetime
from pydantic import BaseModel

from .expense_category import ExpenseCategoryRead


class ExpenseBase(BaseModel):
    description: str
    amount: float


class ExpenseCreate(ExpenseBase):
    category_id: int


class ExpenseRead(ExpenseBase):
    id: int
    timestamp: datetime
    category: ExpenseCategoryRead

    class Config:
        orm_mode = True
