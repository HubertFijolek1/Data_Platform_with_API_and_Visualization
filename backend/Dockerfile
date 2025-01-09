FROM python:3.10-alpine AS builder

WORKDIR /app

ENV PYTHONPATH=/app

# Install build dependencies (Alpine uses apk)
RUN apk add --update --no-cache gcc musl-dev

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-alpine AS final

WORKDIR /app

# Install runtime dependencies (if needed)
# RUN apk add --update --no-cache netcat-openbsd

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entrypoint and CMD
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
