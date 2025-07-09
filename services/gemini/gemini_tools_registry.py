template = {
    "name": "",
    "description": "",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

register_expense = {
    "name": "register_expense",
    "description": """Register an expense given a description, amount and category.
      If the category is not explicitly set in the prompt, choose one that fits from the category list provided. 
      If none of the given categories fits the description, create a new one, following the past categories as examples.
      If there's no given past categories, create a new one following this guidelines:
      - the category should be in lower case
      - should be an atomic word or sentence, like 'comida', 'entretenimiento', 'transporte', 'gastos fijos', and in spanish
      """,
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Description of the expense. For example, 'Gasté 5 soles en pasaje para ir a mi trabajo', 'Compré un almuerzo que costó 25 soles'",
            },
            "amount": {
                "type": "number",
                "description": "Amount of the expense, e.g 34.05, 110, 2000",
            },
            "category_name": {
                "type": "string",
                "description": "Category of the expense. E.g, 'comida', 'entretenimiento', 'gastos fijos'",
            },
        },
        "required": ["description", "amount"],
    },
}
get_list_of_expenses = {
    "name": "get_expenses_list",
    "description": """List the expenses registered by the user.
        The prompt may include:
            - A delta time expression to specify the time range for the expenses (e.g., “últimos X días”, “último mes”, “últimas 2 semanas”).
            - An expense category (e.g., food, transport). This category should be mapped to the user's known or personalized expense categories.
        Delta time interpretation rules:
            - "últimos X días" → past X days
            - "último mes" → past 30 days
            - "últimas 2 semanas" → past 14 days
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
            "category_name": {
                "type": "string",
                "description": "Category of the expense. E.g, 'comida', 'entretenimiento', 'gastos fijos'",
            },
        },
        "required": ["delta_time"],
    },
}


def get_tools():
    return [register_expense, get_list_of_expenses]
