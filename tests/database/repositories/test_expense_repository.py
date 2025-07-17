from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.repositories import expense as expense_repository
from database.schemas.expense import ExpenseCreate
from database.models.user import User
from database.models.expense_category import ExpenseCategory


def test_create_expense(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    assert expense_category_factory.id is not None
    assert user_factory.id is not None
    expense_data = ExpenseCreate(
        description="Lunch",
        amount=12.50,
        category_id=expense_category_factory.id,
    )
    expense = expense_repository.create_expense(
        db_session,
        expense_data,
        user_factory.id,
    )

    assert bool(expense.description == "Lunch")
    assert bool(expense.amount == 12.50)
    assert bool(expense.user_id == user_factory.id)
    assert bool(expense.category_id == expense_category_factory.id)


def test_get_user_expenses(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    assert expense_category_factory.id is not None
    assert user_factory.id is not None
    expense_data1 = ExpenseCreate(
        description="Lunch",
        amount=12.50,
        category_id=expense_category_factory.id,
    )
    expense_repository.create_expense(db_session, expense_data1, user_factory.id)

    expense_data2 = ExpenseCreate(
        description="Dinner",
        amount=25.00,
        category_id=expense_category_factory.id,
    )
    expense_repository.create_expense(db_session, expense_data2, user_factory.id)

    start_date = datetime.now() - timedelta(days=1)
    expenses = expense_repository.get_user_expenses(
        db_session, user_factory.id, start_date=start_date
    )
    assert len(expenses) == 2


def test_get_user_expenses_with_category_filter(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    assert user_factory.id is not None
    assert expense_category_factory.id is not None
    category2 = ExpenseCategory(name="Groceries", user_id=user_factory.id)
    db_session.add(category2)
    db_session.commit()
    assert category2.id is not None

    expense_data1 = ExpenseCreate(
        description="Lunch",
        amount=12.50,
        category_id=expense_category_factory.id,
    )
    expense_repository.create_expense(db_session, expense_data1, user_factory.id)

    expense_data2 = ExpenseCreate(
        description="Milk",
        amount=3.00,
        category_id=category2.id,
    )
    expense_repository.create_expense(db_session, expense_data2, user_factory.id)

    start_date = datetime.now() - timedelta(days=1)
    expenses = expense_repository.get_user_expenses(
        db_session,
        user_factory.id,
        start_date=start_date,
        category_ids=[expense_category_factory.id],
    )
    assert len(expenses) == 1
    assert expenses[0].description == "Lunch"


def test_delete_expense(
    db_session: Session, user_factory: User, expense_category_factory: ExpenseCategory
):
    assert expense_category_factory.id is not None
    assert user_factory.id is not None
    expense_data = ExpenseCreate(
        description="Coffee",
        amount=4.50,
        category_id=expense_category_factory.id,
    )
    expense = expense_repository.create_expense(
        db_session,
        expense_data,
        user_factory.id,
    )

    assert expense.id is not None
    deleted_expense = expense_repository.delete_expense(db_session, expense.id)
    assert deleted_expense is not None
    assert deleted_expense.id == expense.id

    retrieved_expense = expense_repository.get_expense(db_session, expense.id)
    assert retrieved_expense is None
