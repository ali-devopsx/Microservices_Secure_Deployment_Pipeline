#!/bin/bash

# Stop the script if any command fails
set -e

echo "================================================"
echo "🚀 Starting Entrypoint script Execution..."
echo "================================================"

# Check if DB variables exist
: "${DB_HOST:?DB_HOST is not set}"
: "${DB_PORT:?DB_PORT is not set}"

echo "⏳ Waiting for PostgreSQL database to start on ${DB_HOST}:${DB_PORT}..."

# Wait until database is ready
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "⏳ Database is not ready yet... waiting"
  sleep 2
done

echo "✅ PostgreSQL is up and running! Proceeding..."

# =========================================
# 1. Apply database migrations
# =========================================
echo "🎨 [1/3] Applying database migrations..."

# Apply migrations to database
python manage.py migrate --no-input


# =========================================
# 2. Collect static files
# =========================================
echo "📦 [2/3] Collecting static files..."

# Collect all static files into one folder
python manage.py collectstatic --noinput


# =========================================
# 3. Start Gunicorn Server
# =========================================
echo "🔥 [3/3] Starting Gunicorn Web Server..."
echo "===================================================="

# Start Gunicorn (Production server)
exec gunicorn \
    --bind 0.0.0.0:8000 \        # Listen on all network interfaces on port 8000
    --workers $(nproc) \         # Number of worker processes = number of CPU cores
    --timeout 120 \              # Kill worker if request takes more than 120 seconds
    --access-logfile - \         # Print access logs to stdout (Docker logs)
    --error-logfile - \          # Print error logs to stdout
    cyber_portfolio.wsgi:application   # Django WSGI app (entry point)
