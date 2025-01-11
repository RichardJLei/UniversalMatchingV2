# Use Python 3.12 slim image
FROM python:3.12-slim

# Accept build argument
ARG FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files first for better caching
COPY requirements.txt .

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=${FLASK_ENV}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV FLASK_APP=app:app

# Create necessary directories
RUN mkdir -p /app/config /app/logs

# Set permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 8080

# Use a startup script
COPY scripts/startup.sh /startup.sh
RUN chmod +x /startup.sh

# Run the application with proper health check configuration
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