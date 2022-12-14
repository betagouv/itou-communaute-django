#!/bin/sh
set -e

while ! pg_isready -h $POSTGRESQL_ADDON_HOST -p $POSTGRES_PORT; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

django-admin migrate

# --nopin disables for you the annoying PIN security prompt on the web
# debugger. For local dev only of course!
python manage.py runserver_plus 0.0.0.0:8000 --nopin

exec "$@"
