# Dockerfile
FROM python:3.12-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev netcat-openbsd gcc \
    && apt-get clean

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .



RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run using Uvicorn (hot-reload for development)
CMD ["uvicorn", "Nexconnect.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
