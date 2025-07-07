import pandas as pd
from sqlalchemy.orm import Session
from database.models import Expense

def generate_expense_report(db: Session):
    """
    Generates an Excel report of expenses.

    Args:
        db: The database session.

    Returns:
        A pandas DataFrame containing the expenses.
    """
    expenses = db.query(Expense).all()
    data = [{
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
        "timestamp": expense.timestamp
    } for expense in expenses]
    df = pd.DataFrame(data)
    return df
