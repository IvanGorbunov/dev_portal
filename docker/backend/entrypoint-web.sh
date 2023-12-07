#!/bin/sh

# Для БД на хосте
#netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2" host.docker.internal"}' >> /etc/hosts

# На случай если БД бдует долго запускаться
#while ! curl postgres:5432/ 2>&1 | grep '52'; do sleep 1; done

until cd ./src
do
    echo "Waiting for server volume..."
done


# Миграции и статика
until python manage.py makemigrations $1 $2 && python manage.py migrate $1 $2
do
    echo "Waiting for db to be ready..."
    sleep 2
done
python manage.py collectstatic --no-input --clear $1 $2
django-admin makemessages --all --ignore=venv
django-admin compilemessages --ignore=venv

# User credentials
user=admin
email=admin@example.com
password=admin123
echo "from apps.users.models import User; (User.objects.create_superuser('$user', '$email', '$password', role='super_admin')) if not User.objects.filter(role='super_admin').exists() else False" | python3 manage.py shell
#echo "from apps.users.models import User; (User.objects.create_superuser(email='$email', password='$password', role='super_admin', is_verified=True)) if not User.objects.filter(email='$email').exists() else False" | python3 manage.py shell $1 $2

# Запуск воркеров по очередям
#celery -A settings multi start --beat w.no_queue w.low w.high w.flow --loglevel=info --logfile=../logs/%n.log --pidfile=../pids/%n.pid -Q:w.high high -Q:w.low low -Q:w.flow flow


# Запуск самого проекта
#gunicorn clients_portal.wsgi:application --chdir /clients_portal/src/ --bind 0.0.0.0:8000 --workers 2 --timeout 900 --error-logfile ../logs/gunicorn_web_error.log
python manage.py runserver 0.0.0.0:8000 $1 $2

exec "$@"