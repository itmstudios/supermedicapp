#!/bin/sh
set -e

# переходим в каталог Django-проекта
cd /app/supermediconline

echo "Apply database migrations..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn using your wsgi.py..."
# модуль – это supermediconline.wsgi, потому что в manage.py DJANGO_SETTINGS_MODULE выставлен на supermediconline.settings
exec gunicorn supermediconline.wsgi:application --bind 0.0.0.0:8000
