"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging

import environ
import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

logging.basicConfig(level=env.str('DJANGO_LOG_LEVEL', default=logging.INFO), format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 2


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)
SQL_DEBUG = env.bool('SQL_DEBUG', False)
RUN_IN_DOCKER = env.bool('RUN_IN_DOCKER', False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://localhost'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'django_bootstrap5',

    'crispy_forms',
    'crispy_bootstrap5',

    'apps.users.apps.UsersConfig',
    'apps.changelog',
    'apps.clients',
    'apps.clients_requests',
    'apps.products',
    'apps.store',
    'apps.article',

    'drf_yasg',
    'debug_toolbar',
    'admin_extra_buttons',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.changelog.middleware.LoggedInUserMiddleware',
]
if SQL_DEBUG:
    MIDDLEWARE = MIDDLEWARE + ['utils.middleware.DebugQuerysetsWare']
if DEBUG:
    MIDDLEWARE = MIDDLEWARE + ['debug_toolbar.middleware.DebugToolbarMiddleware',]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.store.context_processors.price_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'


# region Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
elif env.str('DATABASE_URL', None):
    DATABASES = {
        'default': env.db(var='DATABASE_URL_IN_DOCKER') if RUN_IN_DOCKER else env.db(),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env.str('SQL_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': env.str('SQL_DATABASE', os.path.join(BASE_DIR, "../db.sqlite3")),
            'USER': env.str('SQL_USER', 'user'),
            'PASSWORD': env.str('SQL_PASSWORD', 'password'),
            'HOST': env.str('SQL_HOST', 'localhost'),
            'PORT': env.str('SQL_PORT', '5432'),
        }
    }
# endregion

# region REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}
# endregion

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'clients_requests:list'
LOGOUT_REDIRECT_URL = 'users:index'
LOGIN_URL = 'users:index'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

MIN_PASSWORD_LENGTH = 8
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': MIN_PASSWORD_LENGTH,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'utils.validators.NumberValidator',
        'OPTIONS': {
            'min_digits': 1,
        },
    },
    {
        'NAME': 'utils.validators.UppercaseValidator',
    },
    {
        'NAME': 'utils.validators.LowercaseValidator',
    },
    {
        'NAME': 'utils.validators.DontRepeatValidator',
        'OPTIONS': {
            'history': 10,
        },
    },
]

# region tz

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# endregion

# region translation

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# endregion

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env.str('STATIC_ROOT', '')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = env.str('MEDIA_ROOT', default=str(ROOT_DIR('media')))
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# region SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env.str('EMAIL_USE_SSL', False)
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = env.str('EMAIL_PORT', 0)
EMAIL_ADR_REGISTRATION = env.str('EMAIL_ADR_REGISTRATION', None)
# endregion

# region Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

REDIS_HOST = env.str('REDIS_HOST', 'redis')
REDIS_PORT = env.str('REDIS_PORT', '6379')
REDIS_DB = "0"

if not RUN_IN_DOCKER:
    REDIS_HOST = env.str('REDIS_HOST_LOCAL', '6379')
    REDIS_PORT = env.str('REDIS_PORT_LOCAL', '6379')

CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/1',
        }
}
# endregion

# region Celery
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'  #env.str('CELERY_BROKER_URL')
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'  # env.str('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_CACHE_BACKEND = 'default'
# CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'   # env.str('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = env.str('CELERY_TASK_SERIALIZER', '')
CELERY_RESULT_SERIALIZER = env.str('CELERY_RESULT_SERIALIZER', '')
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', '')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# endregion

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


SENTRY_DSN = env.str('SENTRY_DSN', None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

USER_CONFIRMATION_KEY = "user_confirmation_{token}"
USER_CONFIRMATION_TIMEOUT = 300
