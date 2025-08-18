# Base image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Entrypoint command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]