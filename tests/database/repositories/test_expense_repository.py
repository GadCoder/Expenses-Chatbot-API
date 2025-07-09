from sqlalchemy.orm import Session
from database.repositories import expense as expense_repository
from database.schemas.expense import ExpenseCreate
from database.models.user import User
from database.models.expense_category import ExpenseCategory


def test_create_expense(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    expense_data = ExpenseCreate(
        description="Lunch",
        amount=12.50,
        category_id=expense_category_factory.id,  # type: ignore
    )
    expense = expense_repository.create_expense(
        db_session,
        expense_data,
        user_factory.id,  # type: ignore
    )

    assert bool(expense.description == "Lunch")
    assert bool(expense.amount == 12.50)
    assert bool(expense.user_id == user_factory.id)
    assert bool(expense.category_id == expense_category_factory.id)


def test_get_user_expenses(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    expense_data1 = ExpenseCreate(
        description="Lunch",
        amount=12.50,
        category_id=expense_category_factory.id,  # type: ignore
    )
    expense_repository.create_expense(db_session, expense_data1, user_factory.id)  # type: ignore

    expense_data2 = ExpenseCreate(
        description="Dinner",
        amount=25.00,
        category_id=expense_category_factory.id,  # type: ignore
    )
    expense_repository.create_expense(db_session, expense_data2, user_factory.id)  # type: ignore

    expenses = expense_repository.get_user_expenses(db_session, user_factory.id)  # type: ignore
    assert len(expenses) == 2
