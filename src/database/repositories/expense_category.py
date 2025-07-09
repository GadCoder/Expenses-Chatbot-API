from sqlalchemy.orm import Session

from database.models.expense_category import ExpenseCategory
from database.schemas.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
)


def create_expense_category(
    db: Session, category: ExpenseCategoryCreate, user_id: int
) -> ExpenseCategory:
    db_category = ExpenseCategory(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_expense_category(db: Session, category_id: int) -> ExpenseCategory | None:
    return db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id).first()


def get_expense_category_by_name(db: Session, name: str) -> ExpenseCategory | None:
    return db.query(ExpenseCategory).filter(ExpenseCategory.name == name).first()


def get_expense_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> list[ExpenseCategory]:
    return db.query(ExpenseCategory).offset(skip).limit(limit).all()


def get_user_expense_categories(db: Session, user_id: int) -> list[ExpenseCategory]:
    return db.query(ExpenseCategory).filter(ExpenseCategory.user_id == user_id).all()


def update_expense_category(
    db: Session, category_id: int, category: ExpenseCategoryUpdate
) -> ExpenseCategory | None:
    db_category = get_expense_category(db, category_id)
    if db_category:
        update_data = category.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_expense_category(db: Session, category_id: int) -> ExpenseCategory | None:
    db_category = get_expense_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
