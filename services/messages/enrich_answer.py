from datetime import datetime


def enrich_answer(function_name: str, answer_data: dict | None) -> str:
    if not answer_data:
        return "No pude procesar tu solicitud :("
    if function_name == "register_expense":
        return enrich_register_expense(answer_data=answer_data)
    return "No pude procesar tu solicitud :("


def enrich_register_expense(answer_data: dict) -> str:
    formated_date = format_date(date=answer_data["timestamp"])
    return f"Se registró el siguiente gasto: \n📌Descripción: {answer_data['description']} \n📌 Monto: {answer_data['amount']} \n📌Categoría: {answer_data['category_name']} \n📌Fecha: {formated_date}"


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
