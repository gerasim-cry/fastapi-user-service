#!/bin/sh
chmod +x entrypoint.sh

echo "Applying migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000