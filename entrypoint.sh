#!/bin/bash
secrethub run --var env=$ENV -- python manage.py migrate
if [ "$ENV" = "dev" ]; then
  secrethub run --var env=$ENV -- python manage.py runserver 0.0.0.0:8765 ;
fi
if [ "$ENV" = "prod" ] || [ "$ENV" = "qa" ]; then
    secrethub run --var env=$ENV -- python manage.py collectstatic --noinput ;
    secrethub run --var env=$ENV -- gunicorn app.wsgi:application --bind 0.0.0.0:$PORT ;
fi
