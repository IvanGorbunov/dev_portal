from django import forms
from django.test import TestCase
from django.contrib.auth import get_user

from apps.clients.tests.factories import ClientFactory
from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.forms import ClientsRequestItemForm, ClientsRequestItemAdminForm
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class ClientsRequestItemFormTest(CustomViewTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_client_1 = UserFactory(
            username='IvanovII',
            fio='Иванов Иван Иванович',
            role=UserRole.CLIENT,
            is_staff=False,
        )
        cls.client_1 = ClientFactory(
            user=cls.user_client_1,
            inn='1234567890',
            name='ИП Иванов Иван Иванович',
        )

    def test_form_field_status(self):
        self.client.login(username='IvanovII', password='adm1n')

        form = ClientsRequestItemForm(user=get_user(self.client))
        self.assertTrue('status' in form.fields)
        self.assertTrue(form.fields['status'].widget.is_hidden)
        self.assertFalse(form.fields['status'].show_hidden_initial)
        self.assertEqual(form.fields['status'].initial, StatusClientsRequest.NEW)

    def test_form_field_is_delete(self):
        self.client.login(username='IvanovII', password='adm1n')

        form = ClientsRequestItemForm(user=get_user(self.client))
        self.assertTrue('is_delete' in form.fields)
        self.assertTrue(form.fields['is_delete'].widget.is_hidden)
        self.assertFalse(form.fields['is_delete'].show_hidden_initial)

    def test_form_field_author(self):
        self.client.login(username='IvanovII', password='adm1n')

        form = ClientsRequestItemForm(user=get_user(self.client))
        self.assertTrue('author' in form.fields)
        self.assertTrue(form.fields['author'].widget.is_hidden)
        self.assertFalse(form.fields['author'].show_hidden_initial)
        self.assertEqual(form.fields['author'].initial, self.client_1)
