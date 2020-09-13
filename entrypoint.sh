#!/bin/bash
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
