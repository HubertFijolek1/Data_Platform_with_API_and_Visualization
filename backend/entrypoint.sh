#!/bin/bash
set -e

# Function to check if the database is ready
function wait_for_db() {
    echo "Waiting for the PostgreSQL database to be ready..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL is up and running!"
}

# Wait for the database
wait_for_db

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic -c alembic.ini upgrade head

# Start the FastAPI server
echo "Starting FastAPI server..."
exec "$@"
