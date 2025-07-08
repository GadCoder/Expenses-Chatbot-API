from sqlalchemy.orm import Session

from database.models.expense import Expense
from database.schemas.expense import ExpenseCreate


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    db_expense = Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()


def get_user_expenses(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[Expense]:
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
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
