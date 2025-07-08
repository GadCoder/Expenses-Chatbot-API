from sqlalchemy.orm import Session

from .tool_registry import register_tool
from database.models.user import User
from .processors.register_expense import register_new_expense


@register_tool
def register_expense(
    db: Session, description: str, amount: float, category_name: str, user: User
):
    return register_new_expense(
        db=db,
        description=description,
        amount=amount,
        category_name=category_name,
        user=user,
    )
