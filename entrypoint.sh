#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Importing countries data..."
python manage.py import_countries || true

echo "Starting server..."
exec gunicorn countriesapp.wsgi:application --bind 0.0.0.0:8000
