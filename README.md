# Expenses Chatbot API

This project is a FastAPI-based chatbot API designed to help users manage their expenses. It integrates with Google's Gemini for natural language processing and can be connected to messaging platforms like WhatsApp.

## Features

- **Expense Tracking:** Register and list expenses through a conversational interface.
- **Natural Language Processing:** Utilizes Google's Gemini to understand user messages.
- **WhatsApp Integration:** Can be connected to a WhatsApp account to act as a chatbot.
- **Secure:** Uses API key authentication and hashes user chat IDs.
- **Containerized:** Can be run using Docker and Docker Compose.

## Getting Started}

### Prerequisites

- Docker
- Docker Compose
- Python 3.12+
- `uv` or `pip` with `venv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/expenses-chatbot-api.git
    cd expenses-chatbot-api
    ```

2.  **Set up your virtual environment:**

    *   **Using `venv` (standard library):**
        ```bash
        python3 -m venv venv
        source .venv/bin/activate
        pip install -r requirements.txt
        ```
    *   **Using `uv`:**
        ```bash
        uv sync
        ```


3.  **Set up the environment variables:**
    -   Create two environment files: `.env.dev` for development and `.env.prod` for production. These files should contain the following variables:
        ```
        ENVIRONMENT=dev/prod

        LLM_PROVIDER=gemini/openai
        LLM_MODEL=your_llm_model
        LLM_API_KEYyour_llm_api_key

        DB_ENGINE=postgresql # or sqlite for development
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=your_db_host
        DB_PORT=your_db_port
        DB_NAME=your_db_name
        ```


### Running the Application

-   **Using Docker (recommended):**
    -   The `run.sh` script simplifies running the application with Docker Compose.
    -   To run in development mode:
        ```bash
        ./run.sh dev
        ```
    -   To run in production mode:
        ```bash
        ./run.sh prod
        ```

-   **Locally (for development):**
    *   **Using `pip`:**
        ```bash
        cd src
        fastapi dev main.py
        ```
    *   **Using `uv`:**
        ```bash
        cd src
        uv run fastapi dev main.py
        ```

## API Endpoints

- **`POST /process-message`**:
  - The main endpoint for processing user messages.
  - **Request Body:**
    ```json
    {
      "chat_id": "user_chat_id",
      "message": "user_message"
    }
    ```
  - **Response:**
    ```json
    {
      "reply": "chatbot_response"
    }
    ```

- **`GET /`**:
  - The root endpoint.
  - **Response:**
    ```json
    {
      "message": "Welcome to the Expenses Chatbot API!"
    }
    ```

## Project Structure

```
.
├── .dockerignore
├── .gitignore
├── .python-version
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── run.sh
├── uv.lock
├── src
│   ├── api
│   │   ├── routers
│   │   │   └── whatsapp.py
│   │   ├── base.py
│   │   └── security.py
│   ├── core
│   ├── database
│   │   ├── models
│   │   ├── repositories
│   │   └── schemas
│   ├── services
│   │   ├── gemini
│   │   ├── messages
│   │   └── processors
│   └── main.py
└── tests
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License
This project is licensed under the terms of the MIT license.