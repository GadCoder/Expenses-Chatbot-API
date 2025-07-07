from core.config import settings


def process_message(message: str, db_session):
    response = chat.send_message(message)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call.function.name
            tool_args = dict(tool_call.function.args)

            if tool_name == "add_expense":
                # Call the actual add_expense function with the db_session
                return (
                    f"Expense '{tool_args.get('description', '')}' added successfully."
                )

    # If no tool was called, return the model's text response
    return response.text
