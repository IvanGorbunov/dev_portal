from django.test import TestCase
from django.contrib.auth import get_user

from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory


class UserViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = UserFactory(
            password='adm1n',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(email=self.user_admin.email, password='adm1n')
        self.assertTrue(get_user(self.client).is_authenticated)
