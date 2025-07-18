from typing import Any, Callable, TypedDict

from src.core.utils import format_date

REGISTER_EXPENSE_EXAMPLES = (
    "_“Gasté 5 soles en pasajes”_ o _“Compré un pollo a la brasa de 55 soles”_"
)

GET_EXPENSES_EXAMPLES = ' _"Dame los gastos de ayer"_ o "_Muéstrame mis gastos de transporte de los últimos 7 días"_'
INSTRUCTION_MESSAGE = (
    "Puedes empezar diciendo algo como:\n"
    f"{REGISTER_EXPENSE_EXAMPLES}\n"
    "También puedes consultar tus gastos diciendo: \n"
    f"{GET_EXPENSES_EXAMPLES}\n"
)

FALLBACK_MESSAGE = (
    "No pude procesar tu solicitud con la información que me diste :( "
    "Por favor, sé un poco más específico para que pueda comprenderte. "
    "Puedes decirme cosas como:\n"
    f"{REGISTER_EXPENSE_EXAMPLES}"
    "También puedes consultar tus gastos diciendo: \n"
    f"{GET_EXPENSES_EXAMPLES}\n"
)


class ExpenseData(TypedDict):
    description: str
    amount: float
    category_name: str
    timestamp: Any


class ExpensesListResult(TypedDict):
    delta_time: int
    expenses: list[ExpenseData]
    categories: list[str]


class UserData(TypedDict):
    user_name: str


def format_expense_data(expense_data: ExpenseData) -> str:
    formatted_date = format_date(date=expense_data["timestamp"])
    return (
        f"\n*{expense_data['description'].capitalize()}* \n"
        f"💰: S/.{expense_data['amount']}\n"
        f"🏷️ Categoría: {expense_data['category_name']} \n"
        f"🗓️: {formatted_date}\n"
    )


def enrich_register_expense(expense_data: ExpenseData) -> str:
    return "Se registró el siguiente gasto:" + format_expense_data(expense_data)


def enrich_get_expenses_list(result: ExpensesListResult) -> str:
    delta_days = result.get("delta_time", 0)
    expenses = result.get("expenses", [])
    categories = result.get("categories", [])

    if not categories:
        category_text = ""
    elif len(categories) == 1:
        category_text = f"para la categoría de {categories[0].capitalize()}"
    else:
        capitalized_categories = [category.capitalize() for category in categories]
        category_text = f"para las categorías de {'/ '.join(capitalized_categories)}"

    if not expenses:
        return (
            f"💸 Aún no tienes gastos registrados{category_text}.\n"
            f"Puedes empezar diciendo algo como:\n{REGISTER_EXPENSE_EXAMPLES}"
        )

    if delta_days == 0:
        base_message = f"*Gastos registrados hoy {category_text}:*\n"
    elif delta_days == 1:
        base_message = f"*Gastos registrados ayer {category_text}:*\n"
    else:
        base_message = (
            f"*Gastos registrados en los últimos {delta_days} días {category_text}:*\n"
        )

    lines = [base_message]
    for expense in expenses:
        lines.append(format_expense_data(expense))

    return "\n".join(lines)


def enrich_welcome_message(user: UserData) -> str:
    user_name = f", {user['user_name']}" if user.get("user_name") else ""
    return f"👋 Hola{user_name}! Soy un bot para el registro de gastos personales.\n{INSTRUCTION_MESSAGE}"


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
