# Stage 1: Builder
FROM python:3.10-slim-buster AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY api/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ml directory and install it
COPY ml /app/ml
RUN pip install -e ./ml && pip list

# Copy application code and tests
COPY api/app /app/app
COPY api/entrypoint.sh /app/entrypoint.sh
COPY alembic.ini /app/alembic.ini
COPY alembic_migrations /app/alembic_migrations
COPY api/tests /app/tests

ENV PYTHONPATH=/app

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Stage 2: Final Image
FROM python:3.10-slim-buster

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code from builder
COPY --from=builder /app/app /app/app
COPY --from=builder /app/entrypoint.sh /app/entrypoint.sh
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/alembic_migrations /app/alembic_migrations

# Copy the tests directory if needed
COPY --from=builder /app/tests /app/tests

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Entrypoint and CMD
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
