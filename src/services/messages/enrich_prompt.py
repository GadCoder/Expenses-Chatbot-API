import re
import textwrap

from sqlalchemy.orm import Session

from database.models.message_history import MessageHistory
from database.repositories.expense_category import get_user_expense_categories


def enrich_prompt(
    db: Session, message: str, user_id: int, message_history: list[MessageHistory]
) -> str:
    history_str = create_message_history_str(message_history=message_history)
    user_categories = get_user_expense_categories(db=db, user_id=user_id)
    user_categories_text = create_user_categories_text(user_categories=user_categories)

    enriched_prompt = f"""
        This is the main content of this request: \n
            - {message}\n
        Use the main content of the current request to determine which function to call.
        If the request is ambiguous or lacks sufficient detail, refer to the message history provided below to add context.
        For example, if the current request is “Ahora de ropa” and the previous message was “Dame el listado de gastos de comida”, it's likely the user now wants the list of expenses for clothes.
        You can also extract details like time period from the previous messages. For instance, if the earlier request specified a time frame (e.g., “de los últimos 7 días”), and the new request omits it, you may use the prior time frame to fill in the gap.
        This is just one example of how message history can help improve understanding.
        Important: Always prioritize the main content of the current request. Use the message history only when necessary to clarify or supplement the intent.
        \n{history_str}
        \n{user_categories_text}
        """

    return textwrap.dedent(text=enriched_prompt)


def create_message_history_str(message_history: list[MessageHistory]) -> str:
    if not message_history:
        return ""
    history_str = ""
    history_str = (
        "MESSAGE HISTORY: This are the last 10 messages from oldest no newer\n"
    )
    for index, msg in enumerate(message_history):
        history_str += f"{index + 1}. {msg.sender_type}: {msg.message}\n"
    history_str = clean_history_text(history_text=history_str)
    return history_str


def clean_history_text(history_text: str) -> str:
    emoji_pattern = re.compile(
        "["  # Start of character group
        "\U0001f600-\U0001f64f"  # Emoticons
        "\U0001f300-\U0001f5ff"  # Symbols & Pictographs
        "\U0001f680-\U0001f6ff"  # Transport & Map Symbols
        "\U0001f1e0-\U0001f1ff"  # Flags
        "\U00002500-\U00002bef"  # Chinese/Japanese/Korean characters
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2b55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # Dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )

    # Remove emojis
    text = emoji_pattern.sub(r"", history_text)

    # Remove symbols like * and _ (keep letters, digits, and spaces)
    text = re.sub(r"[^\w\s]", "", text)

    return text


def create_user_categories_text(user_categories: list) -> str:
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
    return content
