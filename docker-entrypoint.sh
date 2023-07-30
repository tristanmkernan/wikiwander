#!/bin/bash
set -e

if [ "$SKIP_ENTRYPOINT" = "true" ]; then
  echo "Skipping entrypoint..."
  exec "$@"
else
  echo "Running the regular entrypoint..."
  python manage.py collectstatic --no-input
  python manage.py migrate

  gunicorn --workers=2 --bind=0.0.0.0:8000 wikiwander.wsgi
fi
