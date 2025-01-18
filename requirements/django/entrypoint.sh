#!/bin/bash -x

python3 /var/www/django/manage.py makemigrations --noinput || exit 1
python3 /var/www/django/manage.py migrate --noinput || exit 1
python3 /var/www/django/manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 8001 mysite.asgi:application
