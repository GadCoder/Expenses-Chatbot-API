from sqlalchemy.orm import Session

from database.models.user import User
from .tool_registry import register_tool
from .processors import (
    register_expense as _register_expense,
    get_expenses_list as _get_expenses_list,
)


@register_tool
def register_expense(
    db: Session, description: str, amount: float, category_name: str, user: User
):
    return _register_expense(
        db=db,
        description=description,
        amount=amount,
        category_name=category_name,
        user=user,
    )


@register_tool
def get_expenses_list(
    db: Session, delta_time: int, user: User, category_name: str | None = None
):
    return _get_expenses_list(
        db=db, delta_time=delta_time, user=user, category_name=category_name
    )
