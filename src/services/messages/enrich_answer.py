from datetime import datetime


def enrich_answer(function_name: str, result: dict | None) -> str:
    if not result:
        return "No pude procesar tu solicitud :("
    if function_name == "register_expense":
        return enrich_register_expense(expense_data=result)
    if function_name == "get_expenses_list":
        return enrich_get_expenses_list(result=result)
    return "No pude procesar tu solicitud :("


def format_expense_data(expense_data: dict) -> str:
    formated_date = format_date(date=expense_data["timestamp"])
    return f"\n*{expense_data['description']}* \n💰: S/.{expense_data['amount']} soles \n🏷️ Categoría: {expense_data['category_name']} \n🗓️: {formated_date}\n\n"


def enrich_register_expense(expense_data: dict) -> str:
    return "Se registró el siguiente gasto:" + format_expense_data(
        expense_data=expense_data
    )


def format_date(date: datetime) -> str:
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
    if delta_days == 1:
        base_message = "*Gastos de ayer:*\n"
    else:
        base_message = f"Gastos de los últimos {delta_days} días:\n"
    for expense_data in result["expenses"]:
        base_message += format_expense_data(expense_data=expense_data)
    return base_message
