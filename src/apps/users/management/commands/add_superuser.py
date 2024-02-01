import logging

from django.core.management.base import BaseCommand

from apps.users.models import User


LOG = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create admin user'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        LOG.info(f'Superuser creation started.')
        try:
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                role='super_admin',
                is_active=True,
                is_staff=True,
            )
        except Exception as ex:
            LOG.error(f'Can`t create superuser: {ex}')
        finally:
            LOG.info(f'Superuser creation ended.')
