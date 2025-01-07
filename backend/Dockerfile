# backend/Dockerfile

# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ /app/app/
COPY alembic/ /app/alembic/
COPY logging.conf /app/logging.conf

# Expose port
EXPOSE 8000

# Entry point script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
