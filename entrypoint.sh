#!/bin/bash

set -e

echo "================================================"
echo "Starting Entrypoint script Execution..."
echo "================================================"

: "${DB_HOST:?DB_HOST is not set}"
: "${DB_PORT:?DB_PORT is not set}"
: "${DB_USER:?}"
: "${DB_PASSWORD:?}"
: "${DB_NAME:?}"

echo "Waiting for PostgreSQL database to start on ${DB_HOST}:${DB_PORT}..."

# Wait for PostgreSQL to be ready
sleep 10

echo "PostgreSQL should be up. Proceeding..."

echo "[1/3] Applying database migrations..."
python manage.py migrate --no-input

echo "[2/3] Collecting static files..."
python manage.py collectstatic --noinput

echo "[3/3] Starting Gunicorn Web Server..."
echo "===================================================="

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers $(nproc) \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    cyber_portfolio.wsgi:application
