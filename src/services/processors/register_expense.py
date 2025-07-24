from datetime import datetime
from zoneinfo import ZoneInfo
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
    db: Session,
    description: str,
    amount: float,
    category_name: str,
    user: User,
    date: str | None = None,
) -> dict:
    category = expense_category_repository.get_expense_category_by_name(
        db=db, name=category_name
    )
    if not category:
        new_category = expense_category_schema.ExpenseCategoryCreate(name=category_name)
        category = expense_category_repository.create_expense_category(
            db=db,
            category=new_category,
            user_id=user.id,
        )

    parsed_date = None
    if date:
        parsed_date = parse_date_string(date)

    expense_data = expense_schema.ExpenseCreate(
        description=description,
        amount=amount,
        category_id=category.id,
        timestamp=parsed_date,
    )
    registered_expense = expense_repository.create_expense(
        db=db,
        expense=expense_data,
        user_id=user.id,
    )
    result = registered_expense.__dict__.copy()
    result["category_name"] = category_name
    return result


def parse_date_string(date_str: str) -> datetime:
    date_str = date_str.strip()
    formats = [
        "%d/%m/%y",  # 22/07/25
        "%d/%m/%Y",  # 22/07/2025
        "%d-%m-%y",  # 22-07-25
        "%d-%m-%Y",  # 22-07-2025
    ]

    for fmt in formats:
        try:
            naive_dt = datetime.strptime(date_str, fmt)
            lima_dt = naive_dt.replace(tzinfo=ZoneInfo("America/Lima"))
            return lima_dt.astimezone(ZoneInfo("UTC"))
        except ValueError:
            continue

    raise ValueError(
        f"Unable to parse date '{date_str}'. Expected formats: DD/MM/YY, DD/MM/YYYY, DD-MM-YY, DD-MM-YYYY"
    )
