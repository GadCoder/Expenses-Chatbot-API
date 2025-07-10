import logging
from typing import List

from sqlalchemy.orm import Session

from database.models.user import User
from database.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate) -> User:
    logger.info(f"Creating user for chat_id: {user.chat_id}")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with id: {db_user.id}")
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    logger.debug(f"Getting user with id: {user_id}")
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> List[User]:
    logger.debug("Getting all users")
    return db.query(User).all()


def get_user_by_chat_id(db: Session, chat_id: str) -> User | None:
    logger.debug(f"Getting user with chat_id: {chat_id}")
    user = db.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        logger.info(f"User with chat_id: {chat_id} not found. Creating new user.")
        new_user = UserCreate(chat_id=chat_id)
        user = create_user(db=db, user=new_user)
    return user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User | None:
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> User | None:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
