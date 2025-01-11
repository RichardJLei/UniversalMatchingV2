# Use Python 3.12 slim image
FROM python:3.12-slim

# Accept build argument
ARG FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-traditional \
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

# Copy and set up startup script
COPY scripts/startup.sh /startup.sh
RUN chmod +x /startup.sh

# Use the startup script as entrypoint
ENTRYPOINT ["/startup.sh"] 