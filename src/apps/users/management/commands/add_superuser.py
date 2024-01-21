from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Create admin user'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            role='super_admin',
            is_active=True,
            is_staff=True,
        )
