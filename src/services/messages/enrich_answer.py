from typing import Any, Callable, TypedDict

from src.core.utils import format_date

FALLBACK_MESSAGE = "No pude procesar tu solicitud :("
EXPENSE_EXAMPLES = (
    "_“Gasté 5 soles en pasajes”_ o _“Compré un pollo a la brasa de 55 soles”_"
)
INSTRUCTION_MESSAGE = (
    'Puedes empezar diciendo algo como: \n_“Gasté 5 soles en pasajes”_ o _“Compré un pollo a la brasa de 55 soles"_ para registrar un gasto.\n'
    'También puedes consultar tus gastos diciendo _"Dame los gastos de ayer"_ o "_Dame los gastos de la semana pasada"_'
)


class ExpenseData(TypedDict):
    description: str
    amount: float
    category_name: str
    timestamp: Any


class ExpensesListResult(TypedDict):
    delta_time: int
    expenses: list[ExpenseData]
    category_name: str


class UserData(TypedDict):
    user_name: str


# --- Formatter Functions ---


def format_expense_data(expense_data: ExpenseData) -> str:
    formatted_date = format_date(date=expense_data["timestamp"])
    return (
        f"\n*{expense_data['description'].capitalize()}* \n"
        f"💰: S/.{expense_data['amount']}\n"
        f"🏷️ Categoría: {expense_data['category_name']} \n"
        f"🗓️: {formatted_date}\n\n"
    )


def enrich_register_expense(expense_data: ExpenseData) -> str:
    return "Se registró el siguiente gasto:" + format_expense_data(expense_data)


def enrich_get_expenses_list(result: ExpensesListResult) -> str:
    delta_days = result.get("delta_time", 0)
    expenses = result.get("expenses", [])
    category_name = result.get("category_name", "")

    category_text = (
        f" para la categoría de {category_name.capitalize()}" if category_name else ""
    )

    if not expenses:
        return (
            f"💸 Aún no tienes gastos registrados{category_text}.\n"
            f"Puedes empezar diciendo algo como:\n{EXPENSE_EXAMPLES}"
        )

    if delta_days == 0:
        base_message = f"*Gastos registrados hoy{category_text}:*\n"
    elif delta_days == 1:
        base_message = f"*Gastos registrados ayer{category_text}:*\n"
    else:
        base_message = (
            f"*Gastos registrados en los últimos {delta_days} días{category_text}:*\n"
        )

    lines = [base_message]
    for expense in expenses:
        lines.append(format_expense_data(expense).strip())

    return "\n".join(lines)


def enrich_welcome_message(user: UserData) -> str:
    user_name = f", {user['user_name']}" if user.get("user_name") else ""
    return f"👋 Hola{user_name}! Soy un bot para el registro de gastos personales.\n{INSTRUCTION_MESSAGE}"


# --- Dispatcher ---

ENRICH_FUNCTIONS: dict[str, Callable[[Any], str]] = {
    "register_expense": enrich_register_expense,
    "get_expenses_list": enrich_get_expenses_list,
    "welcome_message": enrich_welcome_message,
}


def enrich_answer(function_name: str, answer: dict | None) -> str:
    if not answer:
        return FALLBACK_MESSAGE

    enrich_function = ENRICH_FUNCTIONS.get(function_name)

    if not enrich_function:
        return FALLBACK_MESSAGE

    return enrich_function(answer)
