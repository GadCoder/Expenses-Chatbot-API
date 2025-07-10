from sqlalchemy.orm import Session

from database.models.user import User



def welcome_message(db: Session, user: User) -> dict:
   return {
      "user_name": user.name
   }

