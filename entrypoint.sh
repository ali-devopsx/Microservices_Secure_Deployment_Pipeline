#!/bin/bash


# Exit immediately if a command exits with a non-zero status

set -e

echo "================================================"
echo "🚀 Starting Entrypoint script Execution..."
echo "================================================"


# 1. Apply database migrations
echo "🎨 [1/3] Applying database migrations..."
python manage.py migrate --no-input

# 2. Collect static files
echo "📦 [2/3] Collecting static files..."
python manage.py collectstatic --noinput

# 3. Start Gunicorn Server
echo "🔥 [3/3] Starting Gunicorn Web Server..."
echo "===================================================="

exec gunicorn --bind 0.0.0.0:8000 cyber_portfolio.wsgi:application --workers 4
