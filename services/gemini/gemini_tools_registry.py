from typing import List

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


def get_tools():
    return [register_expense]
