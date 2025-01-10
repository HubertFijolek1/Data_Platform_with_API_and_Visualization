#!/bin/bash

# Wait for the PostgreSQL database to be ready
echo "Waiting for the PostgreSQL database to be ready..."
until pg_isready -h "db" -p 5432; do
  sleep 1
done
echo "PostgreSQL is up and running!"

# Run Alembic migrations from the correct directory
echo "Running Alembic migrations..."
# Changed this line to run from the correct location
if alembic -c /app/alembic.ini upgrade head; then
   echo "Alembic migrations completed successfully."
else
   echo "Alembic migrations failed."
   exit 1
fi

# Start the FastAPI application using uvicorn
echo "Starting the FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
