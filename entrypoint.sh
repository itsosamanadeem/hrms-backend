#!/bin/bash
set -e

# Use environment variables or defaults
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-hrms}"
DB_NAME="${DB_NAME:-postgres}"

echo "📦 Starting HRMS Service Initialization..."
echo "ℹ️ Connecting to database: $DB_NAME as user: $DB_USER"

# Wait for PostgreSQL to be ready
export PGPASSWORD="$DB_PASSWORD"
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"; do
  echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT/$DB_NAME..."
  sleep 2
done

echo "✅ PostgreSQL is ready."

# Activate Python virtual environment
echo "🐍 Activating Python virtual environment..."
source .env/bin/activate

# Export DB info for Python scripts
export DB_HOST DB_PORT DB_USER DB_PASSWORD DB_NAME

# Run initial database setup only once
echo "🛠️  Running initial database setup..."
# python3 -m main
# python -m main

echo "✅ HRMS Base Models Initialized."
echo "🚀 Starting HRMS FastAPI server..."
# exec alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload

