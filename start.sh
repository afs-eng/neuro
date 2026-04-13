#!/bin/bash
echo "🔄 Applying migrations..."
for i in {1..5}; do
    python manage.py migrate --no-input && break
    echo "⏳ Waiting for database to wake up ($i/5)..."
    sleep 5
done

echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application --log-file -