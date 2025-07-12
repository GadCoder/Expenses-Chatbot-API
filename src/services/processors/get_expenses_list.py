from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.models.user import User
from database.repositories import (
    expense as expense_repository,
    expense_category as expense_category_repository,
)


def get_expenses_list(
    db: Session, delta_time: int, user: User, category_name: str | None = None
) -> dict:
    start_date = datetime.now(ZoneInfo("America/Lima")) - timedelta(days=delta_time)
    start_date = start_date.astimezone(ZoneInfo("UTC"))
    category_id = None
    if category_name:
        category = expense_category_repository.get_expense_category_by_name(
            db=db, name=category_name
        )
        if category:
            category_id = category.id

    expenses = expense_repository.get_user_expenses(
        db=db,
        user_id=user.id,  # type: ignore
        start_date=start_date,
        category_id=category_id,  # type: ignore
    )

    result = {"delta_time": delta_time, "expenses": [], "category_name": category_name}
    for expense in expenses:
        expense_data = expense.__dict__
        expense_data["category_name"] = expense.category.name
        result["expenses"].append(expense_data)
    return result
