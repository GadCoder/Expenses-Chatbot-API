from pydantic import BaseModel, ConfigDict


class ExpenseCategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ExpenseCategoryCreate(ExpenseCategoryBase):
    pass


class ExpenseCategoryUpdate(ExpenseCategoryBase):
    pass


class ExpenseCategoryRead(ExpenseCategoryBase):
    id: int
    user_id: int
