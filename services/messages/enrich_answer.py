def enrich_answer(function_name: str, answer_data: dict | None) -> str:
    if not answer_data:
        return "No pude procesar tu solicitud :("
    if function_name == "register_expense":
        return enrich_register_expense(answer_data=answer_data)
    return "No pude procesar tu solicitud :("


def enrich_register_expense(answer_data: dict) -> str:
    return f"""
        Se registró el siguiente gasto: \n
        📌 Descripción: {answer_data["description"]} \n
        📌 Monto: {answer_data["amount"]} \n
        📌 Descripción: {answer_data["category_name"]} \n
        📌 Fecha: {answer_data["timestamp"]} \n
        """
