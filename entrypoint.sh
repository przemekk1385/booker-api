#!/bin/sh

until nc -z -v -w30 postgres 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

./manage.py migrate
./manage.py collectstatic --noinput

exec "$@"
