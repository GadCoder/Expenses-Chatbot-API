from sqlalchemy.orm import Session
from database.models import Expense


def add_expense(db: Session, description: str, amount: float, category: str) -> Expense:
    db_expense = Expense(description=description, amount=amount, category=category)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
