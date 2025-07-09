from sqlalchemy.orm import Session

from database.models.expense_category import ExpenseCategory
from database.schemas.expense_category import ExpenseCategoryUpdate
from database.repositories import expense_category as expense_category_repository


def test_create_expense_category(expense_category_factory: ExpenseCategory):
    assert bool(expense_category_factory.name == "Food")
    assert expense_category_factory.id is not None


def test_get_expense_category(
    db_session: Session, expense_category_factory: ExpenseCategory
):
    retrieved_category = expense_category_repository.get_expense_category(
        db_session, expense_category_factory.id
    )
    assert bool(retrieved_category.id == expense_category_factory.id)


def test_update_expense_category(
    db_session: Session, expense_category_factory: ExpenseCategory
):
    update_data = ExpenseCategoryUpdate(name="Groceries")
    updated_category = expense_category_repository.update_expense_category(
        db_session,
        expense_category_factory.id,  # type: ignore
        update_data,  # type: ignore
    )
    assert bool(updated_category.name == "Groceries")


def test_delete_expense_category(
    db_session: Session, expense_category_factory: ExpenseCategory
):
    deleted_category = expense_category_repository.delete_expense_category(
        db_session,
        expense_category_factory.id,  # type: ignore
    )
    assert deleted_category is not None
    retrieved_category = expense_category_repository.get_expense_category(
        db_session,
        expense_category_factory.id,  # type: ignore
    )
    assert retrieved_category is None
