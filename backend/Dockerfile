# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Accept build argument for environment
ARG FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/logs /secrets

# Copy requirements files first for better caching
COPY requirements.txt .

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn==21.2.0

# Copy environment files first (will be used based on FLASK_ENV)
COPY .env* ./

# Copy application code
COPY . .

# Set base environment variables
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=${FLASK_ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    FLASK_APP=app:app

# Load environment variables from file based on FLASK_ENV
RUN if [ "$FLASK_ENV" = "production" ]; then \
    cp .env.production .env; \
    else \
    cp .env .env; \
    fi

# Set permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --graceful-timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance \
    "app:app" 