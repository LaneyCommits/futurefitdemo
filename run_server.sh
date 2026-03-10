#!/bin/bash
# Start the ExploringU Django server
cd "$(dirname "$0")"
source venv/bin/activate
echo "Starting server at http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop"
python manage.py runserver
