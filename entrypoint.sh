#!/bin/sh
set -e

# Run migrations
export DBWARDEN_CONFIG_MODULE=database
export PYTHONPATH=.
echo "Applying database migrations..."
dbwarden migrate --verbose

# Start application
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8080}"
