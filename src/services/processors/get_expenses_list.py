from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.models.user import User
from database.repositories import (
    expense as expense_repository,
    expense_category as expense_category_repository,
)


def get_expenses_list(
    db: Session, delta_time: int, user: User, categories: list[str] | None = None
) -> dict:
    lima_tz = ZoneInfo("America/Lima")
    now = datetime.now(lima_tz)

    if delta_time == 0:
        # For "today", start from beginning of the current day
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # For other days, go back the specified number of days from now
        start_date = now - timedelta(days=delta_time)

    start_date = start_date.astimezone(ZoneInfo("UTC"))
    category_ids = []
    if categories:
        for category_name in categories:
            category = expense_category_repository.get_expense_category_by_name(
                db=db, name=category_name
            )
            if category:
                category_ids.append(category.id)

    expenses = expense_repository.get_user_expenses(
        db=db,
        user_id=user.id,  # type: ignore
        start_date=start_date,
        category_ids=category_ids,  # type: ignore
    )

    result = {"delta_time": delta_time, "expenses": [], "categories": categories}
    for expense in expenses:
        expense_data = expense.__dict__
        expense_data["category_name"] = expense.category.name
        result["expenses"].append(expense_data)
    return result
