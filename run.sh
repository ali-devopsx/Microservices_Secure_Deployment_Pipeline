#!/bin/bash

# Set environment (default: dev if not provided)
ENV=${1:-dev}
echo "Using environment: $ENV"

# Select the corresponding env file
ENV_FILE=".env.${ENV}"

# Check if the env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Environment file $ENV_FILE not found"
  exit 1
fi
echo "✅ Found env file: $ENV_FILE"

# Copy selected env file to .env (used by Docker Compose)
cp "$ENV_FILE" .env
echo "📄 Copied $ENV_FILE to .env"

# Stop any old containers first
echo "🛑 Stoping old containers..."
docker compose down

# Start serivces in the background
echo "🚀 Starting serivces in the background..."
docker compose up -d --build
