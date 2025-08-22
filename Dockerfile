FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
