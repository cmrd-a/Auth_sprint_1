#!/bin/bash

echo "Waiting for postgres..."
    while ! nc -z "$POSTGRES_DB_PORT" "$POSTGRES_DB_PORT"; do
      sleep 0.1
    done
echo "PostgreSQL started"

gunicorn -k gevent -w 4 wsgi_app:create_app --chdir src/Auth --bind 0.0.0.0:8000
#flask --app src/Auth.app run