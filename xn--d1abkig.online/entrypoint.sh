#!/bin/bash

echo "Apply database migrations..."
python manage.py migrate

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn supermediconline.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4
