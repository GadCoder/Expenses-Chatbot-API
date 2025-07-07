from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from ..database import Base


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")
