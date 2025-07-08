from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.repositories import (
    user as user_repository,
    expense as expense_repository,
    expense_category as expense_category_repository,
)
from database.schemas.expense import ExpenseRead
from database.schemas.expense_category import ExpenseCategoryRead

router = APIRouter()


@router.get("/get-all/")
def get_all_users(db: Session = Depends(get_db)):
    return user_repository.get_all_users(db=db)


@router.get("/{user_id}/expenses", response_model=list[ExpenseRead])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    """Get all expenses for a specific user."""
    return expense_repository.get_user_expenses(db, user_id=user_id)


@router.get("/get-user-categories", response_model=list[ExpenseCategoryRead])
def get_user_categories(user_id: int, db: Session = Depends(get_db)):
    """Get all expense categories for a specific user."""
    return expense_category_repository.get_user_expense_categories(
        db=db, user_id=user_id
    )


@router.get("/get-all-categories", response_model=list[ExpenseCategoryRead])
def get_all_categories(db: Session = Depends(get_db)):
    """Get all expense categories for a specific user."""
    return expense_category_repository.get_expense_categories(db=db)
