import re
import textwrap

from sqlalchemy.orm import Session

from database.models.message_history import MessageHistory
from database.repositories.expense_category import get_user_expense_categories

def enrich_prompt(db: Session, message: str, user_id: int, message_history: list[MessageHistory]) -> str:
    history_str = ""
    if message_history:
        history_str = "MESSAGE HISTORY: This are the last 10 messages from the user in ascendant time order\n"
        for msg in message_history:
            history_str += f"- {msg.sender_type}: {msg.message}\n"
        history_str = clean_history_text(history_text=history_str)
    user_categories = get_user_expense_categories(db=db, user_id=user_id)
    if not user_categories:
        content = """Currently, there's no registered expenses categories. 
        You'll have to define a new one based on the information from the request.
        Some examples are:
            - 'comida': anything food or drinks related
            - 'transporte': like bus ticket pricing or taxis
            - 'entretenmiento': anything related to entertaiment
        - The category should be in lowercase.
        - It should be an atomic word or short phrase in Spanish, such as: "comida", "entretenimiento", "transporte", "gastos fijos".
        Careful when defining a a new expense category. Take into account the full sentence for it.
        For example, 'Comida para mi mascota' at first could seems like 'food', but is actually 'pet'
        """
    else:
        categories_str = ", ".join([str(c.name) for c in user_categories])
        content = f"""This are the existing expense categories registered for this user:
                    [{categories_str}]"""
        
    enriched_prompt = f"""This is the main content of this request: \n
            - {message}\n
        Use the main content of the current request to decide which function to choose.
        If the main request is ambiguous or lacks enough detail, refer to the message history provided below to add context.

        For example, if the current request is “Ahora de ropa” and the previous message was “Dame el listado de gastos de comida”, it’s likely the user now wants the list of expenses for clothes.
        This is just one example of how to use message history to improve understanding.
        
        Important: Always prioritize the main content of the current request. Only use the message history to support or clarify the main request when necessary
        \n{history_str}\n{content}"""
    
    return textwrap.dedent(text=enriched_prompt)

def clean_history_text(history_text: str) -> str:
    emoji_pattern = re.compile(
        "["                     # Start of character group
        "\U0001F600-\U0001F64F" # Emoticons
        "\U0001F300-\U0001F5FF" # Symbols & Pictographs
        "\U0001F680-\U0001F6FF" # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF" # Flags
        "\U00002500-\U00002BEF" # Chinese/Japanese/Korean characters
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"                # Dingbats
        "\u3030"
        "]+", flags=re.UNICODE
    )

    # Remove emojis
    text = emoji_pattern.sub(r'', history_text)

    # Remove symbols like * and _ (keep letters, digits, and spaces)
    text = re.sub(r'[^\w\s]', '', text)

    return text