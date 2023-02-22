# Портал заявок для клиентов

Портал представляет собой сервис для облегчения разрабоки программного обеспечения нескольким командам разработчиков.

## Установка и запуск:

1. Клонировать репозиторий:
   
    ```bash
   git clone ...
   ```
   
1. Создать и заполнить файл`.env` по шаблону `/src/settings/.env.template`. Файл`.env` дожен находится в одной директории с `settings.py`.

   Переменные для заполнения:
   
   - для запуска локально:
      ```
      DEBUG=False
      SQL_DEBUG=False
      
      SECRET_KEY=XXXXXX
     
      EMAIL_USE_TLS=True
      EMAIL_HOST=smtp.gmail.com
      EMAIL_HOST_USER=xxx@gmail.com
      EMAIL_HOST_PASSWORD=***********
      EMAIL_PORT=587
      EMAIL_ADR_REGISTRATION=

      DJANGO_ALLOWED_HOSTS=*

      STATIC_ROOT=var/www/staticfiles

      SENTRY_DSN=
      ```
      
   - для запуска в контейнере `Docker`:
      ```
      DEBUG=False
      SQL_DEBUG=False
      
      SECRET_KEY=XXXXXX
      
      SQL_ENGINE=django.db.backends.postgresql
      SQL_DATABASE=clients_portal
      SQL_USER=postgres
      SQL_PASSWORD=postgres
      SQL_HOST=db
      SQL_PORT=5432
      
      BROKER_URL=redis://redis:6385/0
      
      REDIS_HOST=redis
      REDIS_PORT=6379

      CELERY_ACCEPT_CONTENT=application/json
      CELERY_TASK_SERIALIZER=json
      CELERY_RESULT_SERIALIZER=json
      CELERY_TIMEZONE=Europe/Moscow

      EMAIL_USE_TLS=True
      EMAIL_HOST=smtp.gmail.com
      EMAIL_HOST_USER=xxx@gmail.com
      EMAIL_HOST_PASSWORD=***********
      EMAIL_PORT=587
      EMAIL_ADR_REGISTRATION=

      DJANGO_ALLOWED_HOSTS=*

      STATIC_ROOT=var/www/staticfiles

      SENTRY_DSN=
      ```

1. Установить витуальное окружение для проекта `venv` в директории проекта:
    
   ```bash
   python3 -m venv venv
   ```
   
1. Активировать виртуальное окружение:

   - для Linux: 
       ```bash
       source venv/bin/activate
       ```
   - для Windows:
       ```bash
       .\venv\Scripts\activate.ps1
       ```
     
1. Установить зависимости из `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```
   
1. Выполнить миграции:

    ```bash
    python3 manage.py migrate
    ```
   
1. Собрать статические файлы:

    ```bash
    python3 manage.py collectstatic
    ```
   
1. Запустить сервер:

    ```bash
    python3 manage.py runserver
    ```
   
1. Список эндпоинтов:

   ```angular2html
   http://127.0.0.1:8000/admin/ - административный раздел сайта
   http://127.0.0.1:8000/swagger/ - документация к API сайта
   ```
   
1. Запуск контейнера:

   ```bash
    mkdir -p ./Data/db/
    docker-compose up -d --build
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py migrate"
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py createsuperuser"
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py collectstatic"
    ```
   
1. Запуск тестов в контейнере:

    ```bash
    docker-compose run --rm web ./src/manage.py test
    ```

