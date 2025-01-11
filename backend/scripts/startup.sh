#!/bin/bash
set -e

# Wait for port to be available
timeout 30s bash -c 'until printf "" 2>>/dev/null >>/dev/tcp/$0/$1; do sleep 1; done' localhost 8080

# Start Gunicorn
exec gunicorn --bind :$PORT \
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