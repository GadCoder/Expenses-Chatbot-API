# Use a lightweight Python base image
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock for dependency management
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
RUN uv sync --system

# Copy the rest of your application code
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the rest of your application code
COPY . .

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Set the entrypoint to our script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Command to run your FastAPI application with uvicorn (passed to entrypoint.sh)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
