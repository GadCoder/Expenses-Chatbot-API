#!/bin/bash

# Usage: ./run.sh dev OR ./run.sh prod
ENVIRONMENT="$1"

if [ "$ENVIRONMENT" = "prod" ]; then
  ENV_FILE=".env.prod"
elif [ "$ENVIRONMENT" = "dev" ]; then
  ENV_FILE=".env.dev"
else
  echo "❌ Usage: ./run.sh [dev|prod]"
  exit 1
fi

# Check that the file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Env file $ENV_FILE not found"
  exit 1
fi

export ENV_FILE="$ENV_FILE"
echo "Getting running containers down"
docker compose down

echo "Running Docker Compose with $ENV_FILE"
docker compose --env-file "$ENV_FILE" up --build -d
