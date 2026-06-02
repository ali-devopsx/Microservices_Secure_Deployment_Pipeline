#!/bin/bash

# Set environment (default: dev if not provided)
ENV=${1:-dev}

# Select the corresponding env file
ENV_FILE=".env.${ENV}"

# Check if the env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Environment file $ENV_FILE not found"
  exit 1
fi

# Copy selected env file to .env (used by Docker Compose)
cp "$ENV_FILE" .env




# Start services in detached mode
docker compose down
docker compose up -d --build
