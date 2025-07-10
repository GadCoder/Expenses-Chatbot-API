import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import Base
from database.models.user import User
from database.schemas.user import UserCreate
from database.models.expense_category import ExpenseCategory
from database.schemas.expense_category import ExpenseCategoryCreate
from database.repositories import (
    user as user_repository,
    expense_category as expense_category_repository,
)
from core.security import hash_chat_id


@pytest.fixture(scope="function")
def db_session() -> Session:  # type: ignore
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session  # type: ignore
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def user_factory(db_session: Session) -> User:
    hashed_chat_id = hash_chat_id("12345")
    user_data = UserCreate(chat_id=hashed_chat_id)
    return user_repository.create_user(db_session, user_data)


@pytest.fixture
def expense_category_factory(
    db_session: Session, user_factory: User
) -> ExpenseCategory:
    category_data = ExpenseCategoryCreate(name="Food")
    return expense_category_repository.create_expense_category(
        db_session,
        category_data,
        user_factory.id,  # type: ignore
    )
