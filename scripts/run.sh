#!/bin/sh

set -e # if an portion of the script crash, crash all the code and not continue

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
