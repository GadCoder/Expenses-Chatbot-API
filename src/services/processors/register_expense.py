from sqlalchemy.orm import Session

from database.models.user import User
from database.schemas import (
    expense as expense_schema,
    expense_category as expense_category_schema,
)
from database.repositories import (
    expense as expense_repository,
    expense_category as expense_category_repository,
)


def register_expense(
    db: Session, description: str, amount: float, category_name: str, user: User
) -> dict:
    print("On register expense")
    category = expense_category_repository.get_expense_category_by_name(
        db=db, name=category_name
    )
    if not category:
        new_category = expense_category_schema.ExpenseCategoryCreate(name=category_name)
        category = expense_category_repository.create_expense_category(
            db=db,
            category=new_category,
            user_id=user.id,  # type: ignore
        )
    print(f"User ID: {user.id}")
    print(f"Category: {category.name}")  # type: ignore
    expense_data = expense_schema.ExpenseCreate(
        description=description,
        amount=amount,
        category_id=category.id,  # type: ignore
    )
    registered_expense = expense_repository.create_expense(
        db=db,
        expense=expense_data,
        user_id=user.id,  # type: ignore
    )
    result = registered_expense.__dict__.copy()
    result["category_name"] = category_name
    return result
