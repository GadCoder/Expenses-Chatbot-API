from datetime import datetime
from zoneinfo import ZoneInfo


def enrich_answer(function_name: str, answer: dict | None) -> str:
    if not answer:
        return "No pude procesar tu solicitud :("
    if function_name == "register_expense":
        return enrich_register_expense(expense_data=answer)
    if function_name == "get_expenses_list":
        return enrich_get_expenses_list(result=answer)
    if function_name == "welcome_message":
        return enrich_welcome_message(user=answer)
    return "No pude procesar tu solicitud :("


def format_expense_data(expense_data: dict) -> str:
    formated_date = format_date(date=expense_data["timestamp"])
    return f"\n*{expense_data['description'].capitalize()}* \n💰: S/.{expense_data['amount']}\n🏷️ Categoría: {expense_data['category_name']} \n🗓️: {formated_date}\n\n"


def enrich_register_expense(expense_data: dict) -> str:
    return "Se registró el siguiente gasto:" + format_expense_data(
        expense_data=expense_data
    )


def format_date(date: datetime) -> str:
    date = date.astimezone(ZoneInfo("America/Lima"))
    months = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    day = date.strftime("%d")
    month = months[date.month]
    hour = date.strftime("%H:%M")

    return f"{day} de {month} a las {hour}"


def enrich_get_expenses_list(result: dict) -> str:
    delta_days = result["delta_time"]
    expenses = result["expenses"]
    if not expenses:
        return '💸 Aún no tienes gastos registrados.\nPuedes empezar diciendo algo como: \n_“Gasté 5 soles en pasajes”_ o _“Compré un pollo a la brasa de 55 soles"_'
    if delta_days == 0:
        base_message = "*Gastos registrados hoy:*\n"
    elif delta_days == 1:
        base_message = "*Gastos registrados ayer:*\n"
    else:
        base_message = f"Gastos registrados en los últimos {delta_days} días:\n"
    for expense in expenses:
        base_message += format_expense_data(expense_data=expense)
    return base_message


def enrich_welcome_message(user: dict) -> str:
    user_name = f", {user['user_name']}" if user["user_name"] else ""
    return f'👋 Hola{user_name}! Soy un bot para el registro de gastos personales.\nPuedes empezar diciendo algo como: \n_“Gasté 5 soles en pasajes”_ o _“Compré un pollo a la brasa de 55 soles"_ para registrar un gasto.\nTambién puedes consultar tus gastos diciendo _"Dame los gastos de ayer"_ o "_Dame los gastos de la semana pasada"_'
