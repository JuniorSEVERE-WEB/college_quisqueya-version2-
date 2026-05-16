#!/bin/sh
set -e

echo "=== [start.sh] Begin =================================="
echo "[start.sh] Running collectstatic..."
python backend/manage.py collectstatic --noinput
echo "[start.sh] collectstatic OK."

echo "[start.sh] Starting gunicorn..."
exec gunicorn --pythonpath backend backend.wsgi:application --timeout 120 --workers 2
