#!/bin/sh
set -e

echo "Apply database migrations..."
python ./supermediconline/manage.py migrate --noinput

echo "Collect static files..."
python ./supermediconline/manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn supermediconline.wsgi:application --bind 0.0.0.0:8000
