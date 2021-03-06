#!/bin/sh

echo "Waiting for postgres..."

# Wait until if postgress is reachable
while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0 -p 8000