FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN mkdir -p saved_models  # ensures directory for model storage

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
