import re
import textwrap

from sqlalchemy.orm import Session

from database.models.message_history import MessageHistory
from database.repositories.expense_category import get_user_expense_categories
from ..llm.tools_registry import get_tools


def enrich_prompt(
    db: Session, message: str, user_id: int, message_history: list[MessageHistory]
) -> str:
    available_tools_text = create_available_tools_text()
    current_known_context = get_last_context(message_history=message_history)
    user_categories = get_user_expense_categories(db=db, user_id=user_id)
    history_str = create_message_history_str(message_history=message_history)
    user_categories_text = create_user_categories_text(user_categories=user_categories)

    enriched_prompt = f"""
    You are an assistant that helps users manage their personal expenses via WhatsApp using function calls.

    Your task is to determine the appropriate function to call and its arguments based on the user's current message. 
    If the message is ambiguous or lacks detail, use recent conversation history to infer the user's intent or fill in missing arguments, such as category or time range.

    Available functions to call:
    {available_tools_text}
    Examples:
    - If the user says “Ahora de transporte” after “Muéstrame los gastos de comida de los últimos 7 días”, infer they now want gastos de transporte de los últimos 7 días.
    - If the time range was “de este mes” and the user now says “los de entretenimiento”, assume the same time range.
    - If the current message is “Ahora de ropa” and the previous message was “Dame el listado de gastos de comida”, it's likely the user wants the list of expenses for clothes.

    Guidelines:
    - Always prioritize the current message to determine intent and arguments.
    - Use message history **only when necessary** to clarify or complete the intent.
    - Use only last known context when needed. 
    - Do not fabricate or guess values — only infer based on clear and recent context.
    - If no function should be called, do not return a function call.

    **Conversation history:**
    {history_str}

    *Last known context:*
    {current_known_context}

    **Available categories:**
    {user_categories_text}

    **Current message:**
    \"{message}\"
    """

    return textwrap.dedent(text=enriched_prompt)


def create_message_history_str(message_history: list[MessageHistory]) -> str:
    if not message_history:
        return ""
    history_str = ""
    history_str = "These are the last 10 messages from oldest to newest\n"
    for index, msg in enumerate(message_history):
        history_str += f"{index + 1}. {msg.sender_type}: {msg.message}\n"
    history_str = clean_history_text(history_text=history_str)
    return history_str


def get_last_context(message_history: list[MessageHistory]) -> str:
    if not message_history:
        return "No conversation history available"
    last_bot_message = next(
        (msg for msg in reversed(message_history) if msg.sender_type == "BOT"), None
    )
    if not last_bot_message:
        return "No previous bot context available"

    context_parts = []
    if last_bot_message.categories:
        categories = last_bot_message.categories.strip()
        context_parts.append(f"Previous category(ies): {categories}")
    else:
        context_parts.append("Previous category(ies): None")
    if last_bot_message.delta_time is not None:
        days = last_bot_message.delta_time
        time_desc = _format_time_description(days)
        context_parts.append(f"Previous time range: {days} days ({time_desc})")
    else:
        context_parts.append("Previous time range: None")

    return "\n- " + "\n- ".join(context_parts)


def _format_time_description(days: int) -> str:
    """Convert days to a human-readable time description."""
    if days == 0:
        return "today"
    elif days == 1:
        return "yesterday"
    elif days == 7:
        return "last week"
    elif days == 30:
        return "last month"
    elif days % 7 == 0:
        weeks = days // 7
        return f"last {weeks} week{'s' if weeks > 1 else ''}"
    else:
        return f"last {days} days"


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
        If needed, you'll have to define a new one based on the information from the request.
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
        content = f"These are the existing expense categories registered for this user:[{categories_str}]"
    return content


def create_available_tools_text() -> str:
    if not get_tools():
        return "No tools available."
    tools_text = []
    for tool in get_tools():
        tool_info = [
            f"Function: {tool['name']}",
            f"Description: {tool['description'].strip()}",
        ]

        parameters = tool.get("parameters", {})
        properties = parameters.get("properties", {})
        required = parameters.get("required", [])

        if properties:
            tool_info.append("Parameters:")
            for param_name, param_details in properties.items():
                param_type = param_details.get("type", "unknown")
                param_desc = param_details.get(
                    "description", "No description available"
                )
                required_marker = (
                    " (required)" if param_name in required else " (optional)"
                )
                tool_info.append(
                    f"  - {param_name} ({param_type}){required_marker}: {param_desc}"
                )
        else:
            tool_info.append("Parameters: None")

        tools_text.append("\n".join(tool_info))

    return "\n\n".join(tools_text)
