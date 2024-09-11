#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Aguardando o banco de dados..."
  sleep 1
done

daphne -b 0.0.0.0 -p 8000 mysite.asgi:application