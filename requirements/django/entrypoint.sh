#!/bin/sh

python3 /var/www/django/manage.py makemigrations
python3 /var/www/django/manage.py migrate
python3 /var/www/django/manage.py collectstatic --noinput

#python ../mysite/manage.py runserver 0.0.0.0:8001
daphne -b 0.0.0.0 -p 8001 mysite.asgi:application