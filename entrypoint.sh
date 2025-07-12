#!/bin/bash

set -e

# Optional: install node modules if you have a frontend
if [ -f "package.json" ]; then
  echo "Installing frontend dependencies..."
  npm install
  npm run build
fi

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
