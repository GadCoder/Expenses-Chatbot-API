from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .expense_category import ExpenseCategoryRead


class ExpenseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: str
    amount: float


class ExpenseCreate(ExpenseBase):
    category_id: int


class ExpenseRead(ExpenseBase):
    id: int
    timestamp: datetime
    category: ExpenseCategoryRead
