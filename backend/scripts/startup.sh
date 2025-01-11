#!/bin/bash
set -e

echo "Starting application..."

# Function to check if the application is responding
wait_for_app() {
    echo "Waiting for application to start..."
    for i in {1..30}; do
        if nc -z localhost 8080; then
            echo "Application is ready!"
            return 0
        fi
        echo "Attempt $i: Application is not ready yet..."
        sleep 1
    done
    echo "Application failed to start within timeout"
    return 1
}

# Start Gunicorn in the background
/usr/local/bin/gunicorn --bind :$PORT \
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
    "app:app" &

# Store the Gunicorn PID
GUNICORN_PID=$!

# Wait for the application to be ready
wait_for_app

# If the application didn't start properly, exit
if [ $? -ne 0 ]; then
    echo "Application failed to start"
    kill $GUNICORN_PID
    exit 1
fi

# Wait for Gunicorn to exit
wait $GUNICORN_PID 