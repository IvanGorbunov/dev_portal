import json

from django.db.models import Model
from django.urls import reverse_lazy
from django.test import override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.users.choices import UserRole
from apps.users.models import User
from utils.utils import generate_uniq_code


@override_settings(SQL_DEBUG=False)
class TestCaseBase(APITestCase):
    """
    Базовый (без авторизации)
    """
    CONTENT_TYPE_JSON = 'application/json'

    def check_status(self, response, status):
        self.assertEqual(response.status_code, status, response.data)

    def generate_uniq_code(self):
        return generate_uniq_code()


class WithLoginTestCase(TestCaseBase):
    """
    С авторизацией
    """
    @classmethod
    def setUpClass(cls):
        user, is_create = User.objects.get_or_create(username='admin')
        if is_create:
            user.role = UserRole.SUPER_ADMIN
            user.set_password('admin')
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
        cls.user = user
        super().setUpClass()

    def setUp(self) -> None:
        self.auth_user(self.user)
        super().setUp()

    def auth_user(self, user):
        """
        Авторизация
        """
        self.client.force_authenticate(user)


class CustomViewTestCase(WithLoginTestCase):

    def _test_list(self, url, object):
        if ':' in url:
            url = reverse_lazy(url)
        response = self.client.get(url)
        rows = response.data['results']
        self.assertEqual([row['id'] for row in rows if row['id'] == object.pk], [object.pk])
        self.assertEqual(response.status_code, 200)

    def _test_create(self, url_name, model, check_field, status_code=201):
        url = reverse_lazy(url_name)
        data = self._generate_data()
        response = self.client.post(url, data=json.dumps(data), content_type=self.CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, status_code, response.data)
        object = model.objects.filter(pk=response.data['id']).first()
        self.assertEqual(getattr(object, check_field), data[check_field])
        return object

    def _test_detail(self, url_name: str, object: 'Model', check_field: str = 'id'):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(getattr(object, check_field), response.data[check_field])

    def _test_edit(self, url_name: str, object: 'Model', check_field: str = None, data=None):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        if data is None:
            data = self._generate_data()
        response = self.client.put(url, data=json.dumps(data), content_type=self.CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, 200, response.data)
        object = type(object).objects.filter(pk=response.data['id']).first()
        if check_field:
            self.assertEqual(getattr(object, check_field), data[check_field])
        return object

    def _test_delete(self, url_name, object):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        qs = type(object).objects.filter(pk=object.pk, is_delete=False)
        self.assertIsNone(qs.first())

    def _generate_data(self):
        pass
