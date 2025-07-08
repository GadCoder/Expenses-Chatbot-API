from typing import List

from sqlalchemy.orm import Session

from database.models.user import User
from database.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user_by_chat_id(db: Session, chat_id: str) -> User | None:
    user = db.query(User).filter(User.chat_id == chat_id).first()
    if not user:
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
