import logging
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.models.expense import Expense
from database.schemas.expense import ExpenseCreate

logger = logging.getLogger(__name__)


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    logger.info(f"Creating expense for user_id: {user_id}")
    db_expense = Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    logger.info(f"Expense created with id: {db_expense.id}")
    return db_expense


def get_expense(db: Session, expense_id: int) -> Expense | None:
    logger.debug(f"Getting expense with id: {expense_id}")
    return db.query(Expense).filter(Expense.id == expense_id).first()


def get_user_expenses(
    db: Session,
    user_id: int,
    start_date: datetime,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Expense]:
    logger.debug(f"Getting expenses for user_id: {user_id}")
    filters = [
        Expense.user_id == user_id,
        Expense.timestamp >= start_date,
    ]

    if category_id:
        filters.append(Expense.category_id == category_id)

    return (
        db.query(Expense)
        .filter(*filters)
        .order_by(desc(Expense.timestamp))
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_expense(db: Session, expense_id: int) -> Expense | None:
    db_expense = get_expense(db, expense_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense
