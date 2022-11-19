#!/bin/sh

until nc -z -v -w30 postgres 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

make manage/migrate
make manage/collectstatic

exec "$@"
