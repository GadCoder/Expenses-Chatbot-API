template = {
    "name": "",
    "description": "",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

register_expense = {
    "name": "register_expense",
    "description": """
        Register an expense given a description, amount, expense category, and optionally, a date
        - The date is optional and can be expressed in various formats. For example:
            - A specific date like "12 de julio"
            - A relative expression like "yesterday" or "last Monday"
        - The current datetime will be provided, so you can resolve relative dates accordingly.
        - Use DD/MM/YY or DD/MM/YYYY format for the date (you can also use dashes: DD-MM-YY or DD-MM-YYYY)
        - If the category is not explicitly provided, choose one that best fits from the list of existing categories.
        -  Careful when choosing the expense category. Take into account the full sentence for it.
        For example, 'Comida para mi mascota' at first could seems like 'food', but is actually 'pet'
      """,
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Description of the expense. For example, 'Gasté 5 soles en pasaje para ir a mi trabajo', 'Compré un almuerzo que costó 25 soles', 'Pagué 60 soles por la consulta del veterinario', 'Compré un regalo de cumpleaños por 40 soles', 'Compré un almuerzo que costó 25 soles'",
            },
            "amount": {
                "type": "number",
                "description": "Amount of the expense, e.g 34.05, 110, 2000",
            },
            "category_name": {
                "type": "string",
                "description": "Optional category for the expense. If not provided, the system will infer or generate one E.g, 'comida', 'entretenimiento', 'gastos fijos'",
            },
            "date": {
                "type": "string",
                "description": "Optional date for the expense. If not provided, the system will use the current date. Use DD/MM/YY or DD/MM/YYYY format. Examples: '22/07/25', '22/07/2025', '22-07-25', '22-07-2025'",
            },
        },
        "required": ["description", "amount"],
    },
}

get_list_of_expenses = {
    "name": "get_expenses_list",
    "description": """List the expenses registered by the user.
        The prompt may include:
            - One or more expense categories (e.g., food, transport). This category should be mapped to the user's known or personalized expense categories.
            - A delta time expression to specify the time range for the expenses (e.g., “últimos X días”, “último mes”, “últimas 2 semanas”).
        Delta time interpretation rules:
            - 'Ayer' -> 1 day ago
            - 'Hoy' -> from today, meaning 0 days ago
            - 'Hace X semanas' -> past X * 7 days
            - 'últimos X días' → past X days
            - 'último mes' → past 30 days
            - 'últimas 2 semanas' → past 14 days
        Equivalences:
            - 1 month = 30 days
            - 1 week = 7 days
        Default behavior:
            If no delta time is provided, assume a default of 7 days.
        """,
    "parameters": {
        "type": "object",
        "properties": {
            "delta_time": {
                "type": "number",
                "description": "Number of past days to use as a delta for the expenses registry list. For example, 30, 1, etc",
            },
            "categories": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of categories for the expenses. Could be one or more. E.g, 'comida', 'entretenimiento', 'gastos fijos', 'comida y transporte'",
            },
        },
        "required": ["delta_time"],
    },
}

welcome_message = {
    "name": "welcome_message",
    "description": """Welcomes the user and provides an introduction. 
        This function is triggered whenever the user sends a greeting like:
            - 'Hello'
            - 'Hola'
            - 'Holi'
            - 'Hola causa'
            - 'Buenos días'
            - 'Buenas tardes'
            - 'Oe causa'
        Or any other variation.""",
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def get_tools():
    return [register_expense, get_list_of_expenses, welcome_message]
