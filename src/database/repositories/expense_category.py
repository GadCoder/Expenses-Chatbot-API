import logging
from sqlalchemy.orm import Session

from database.models.expense_category import ExpenseCategory
from database.schemas.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
)

logger = logging.getLogger(__name__)


def create_expense_category(
    db: Session, category: ExpenseCategoryCreate, user_id: int
) -> ExpenseCategory:
    logger.info(f"Creating expense category for user_id: {user_id}")
    db_category = ExpenseCategory(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    logger.info(f"Expense category created with id: {db_category.id}")
    return db_category


def get_expense_category(db: Session, category_id: int) -> ExpenseCategory | None:
    logger.debug(f"Getting expense category with id: {category_id}")
    return db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id).first()


def get_expense_category_by_name(db: Session, name: str) -> ExpenseCategory | None:
    logger.debug(f"Getting expense category with name: {name}")
    return db.query(ExpenseCategory).filter(ExpenseCategory.name == name).first()


def get_expense_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> list[ExpenseCategory]:
    logger.debug("Getting all expense categories")
    return db.query(ExpenseCategory).offset(skip).limit(limit).all()


def get_user_expense_categories(db: Session, user_id: int) -> list[ExpenseCategory]:
    logger.debug(f"Getting expense categories for user_id: {user_id}")
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
