template = {
    "name": "",
    "description": "",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

register_expense = {
    "name": "register_expense",
    "description": """Register an expense given a description, amount and category.
      If the category is not explicitly set in the request, choose one that fits from the category list provided. 
      If none of the given categories fits the description, create a new one, following the past categories as examples.
      If there's no given past categories, create a new one following this guidelines:
      - the category should be in lower case
      - should be an atomic word, like 'comida', 'entretenimiento', 'transporte'
      """,
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Description of the expense",
            },
            "amount": {
                "type": "float",
                "description": "Amount of the expense, e.g 34.05, 110, 2000",
            },
            "category": {
                "type": "string",
                "description": "Category of the expense. E.g, 'comida', 'entretenimiento', 'gastos fijos'",
            },
        },
        "required": ["description", "amount"],
    },
}
