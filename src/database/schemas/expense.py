from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from .expense_category import ExpenseCategoryRead


class ExpenseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float
    description: str
    timestamp: datetime | None = Field(default=None)


class ExpenseCreate(ExpenseBase):
    category_id: int
    timestamp: datetime | None = None


class ExpenseRead(ExpenseBase):
    id: int
    timestamp: datetime
    category: ExpenseCategoryRead
