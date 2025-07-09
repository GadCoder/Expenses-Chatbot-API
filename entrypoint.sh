#!/bin/bash
set -e

# Determine the environment
ENVIRONMENT=${ENVIRONMENT:-dev} # Default to dev if not set

# Create the .env file based on the environment
if [ "$ENVIRONMENT" = "prod" ]; then
  cp .env.prod .env
  echo "Copied .env.prod to .env"
elif [ "$ENVIRONMENT" = "dev" ]; then
  cp .env.dev .env
  echo "Copied .env.dev to .env"
else
  echo "Warning: Unknown ENVIRONMENT '$ENVIRONMENT'. No .env file copied."
fi

# Execute the main command (e.g., uvicorn)
exec "$@"
