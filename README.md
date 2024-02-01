# Software Development Process Management System

---
The project is a website designed to facilitate the process of software development. The system provides for the registration of user requests for feedback on the operation of the software.

### Features:
 - [x] users requests
 - [ ] kanban board
 - [ ] profile of the project
 - [ ] profile of the developers
 - [ ] chat
 - [ ] wiki for projects
 - [x] make a separation by selector layer
 - [x] make a hierarchy of product categories by 'django-cte' 

---
### Installation:

1. Clone the repository:
   
    ```bash
   git clone https://github.com/IvanGorbunov/dev_portal.git
   ```
   
2. Create and fill up a `.env` file according to the template `/src/settings/.env.template`. The `.env` file must be in the same directory as `settings.py`.

   Variables to fill:
   
   - for local run (will be use SQLite database):
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
      
   - for run in container `Docker` (will be use SQLite PostgreSQL):
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

3. Install all necessary package from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```
   
4. Run a migration:

    ```bash
    python3 manage.py migrate
    ```
   
5. Create a superuser:

    ```bash
    python3 manage.py add_superuser
    ```

6. Collect static files:

    ```bash
    python3 manage.py collectstatic
    ```
   
7. Run server:

    ```bash
    python3 manage.py runserver
    ```
   
8. Get a list of endpoints by url:

   ```angular2html
   http://127.0.0.1:8000/admin/ - admin panel
   http://127.0.0.1:8000/swagger/ - documents for API
   ```
   
9. Run containers in Docker`s containers:

   ```bash
    mkdir -p ./Data/db/
    docker-compose up -d --build
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py migrate"
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py createsuperuser"
    docker-compose run --rm web sh -c "cd ./src && python3 manage.py collectstatic"
    ```
   
10. Run tests in Docker`s containers:

     ```bash
     docker-compose run --rm web ./src/manage.py test
     ```

