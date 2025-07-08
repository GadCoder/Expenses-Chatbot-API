from sqlalchemy.orm import Session
from database.repositories.expense_category import get_user_expense_categories


def enrich_prompt(db: Session, message: str, user_id: int) -> str:
    user_categories = get_user_expense_categories(db=db, user_id=user_id)
    if not user_categories:
        content = """Currently, there's no registered expenses categories. 
        You'll have to define a new one based on the information from the request.
        Some examples are:
            - 'comida': anything food or drinks related
            - 'transporte': like bus ticket pricing or taxis
            - 'entretenmiento': anything related to entertaiment
        """
    else:
        categories_str = ", ".join([str(c.name) for c in user_categories])
        content = f"""This are the existing expense categories registered for this user:
                    [{categories_str}]"""

    return f"{message}\n{content}"
