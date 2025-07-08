from pydantic import BaseModel


class ExpenseCategoryBase(BaseModel):
    name: str


class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass


class ExpenseCategoryUpdate(ExpenseCategoryBase):
    pass


class ExpenseCategoryRead(ExpenseCategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
