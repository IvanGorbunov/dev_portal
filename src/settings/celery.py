import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Queue


class CeleryQueues:

    HIGH = 'high'  # Срочные к выполнению (под ней выделен отдельный воркер)
    CELERY = 'celery'  # Общая очередь (после неё выполняется LOW)
    LOW = 'low'  # Можно обработать c опозданием

    ITEMS = (
        Queue(CELERY),
        Queue(HIGH),
        Queue(LOW),
    )


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
app = Celery('clients_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
