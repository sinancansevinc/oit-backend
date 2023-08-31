#!/bin/bash
python manage.py collectstatic --noinput
until python manage.py migrate; do
    echo "Waiting for db to be ready..."
    sleep 1
done
gunicorn oit_backend.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4 --access-logfile '-' --error-logfile '-' --reload