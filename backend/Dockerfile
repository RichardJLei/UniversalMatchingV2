# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements files first for better caching
COPY requirements.txt .
COPY requirements-test.txt .

# Copy application code
COPY . .

# Ensure config directory exists
RUN mkdir -p /app/config

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV GUNICORN_CMD_ARGS="--workers=1 --threads=8 --timeout=0 --log-level=debug --error-logfile=- --access-logfile=-"
ENV PYTHONPATH=/app
ENV FLASK_APP=app:app

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :$PORT "app:app" 