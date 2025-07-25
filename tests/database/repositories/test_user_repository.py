from sqlalchemy.orm import Session

from core.security import hash_chat_id
from database.repositories import user as user_repository
from database.schemas.user import UserCreate, UserUpdate


def test_create_user(db_session: Session):
    hashed_chat_id = hash_chat_id("12345")
    user_data = UserCreate(chat_id=hashed_chat_id)
    user = user_repository.create_user(db_session, user_data)
    assert str(user.chat_id) == hashed_chat_id
    assert user.id is not None


def test_get_user(db_session: Session):
    hashed_chat_id = hash_chat_id("12345")
    user_data = UserCreate(chat_id=hashed_chat_id)
    user = user_repository.create_user(db_session, user_data)
    retrieved_user = user_repository.get_user(db_session, user.id)
    assert retrieved_user.id == user.id


def test_update_user(db_session: Session):
    hashed_chat_id = hash_chat_id("12345")
    user_data = UserCreate(chat_id=hashed_chat_id)
    user = user_repository.create_user(db_session, user_data)
    update_data = UserUpdate(chat_id=hashed_chat_id, name="Obi Wan Kenobi")
    updated_user = user_repository.update_user(db_session, user.id, update_data)
    assert updated_user.name == "Obi Wan Kenobi"


def test_delete_user(db_session: Session):
    hashed_chat_id = hash_chat_id("12345")
    user_data = UserCreate(chat_id=hashed_chat_id)
    user = user_repository.create_user(db_session, user_data)
    deleted_user = user_repository.delete_user(db_session, user.id)
    assert deleted_user is not None
    retrieved_user = user_repository.get_user(db_session, user.id)
    assert retrieved_user is None
