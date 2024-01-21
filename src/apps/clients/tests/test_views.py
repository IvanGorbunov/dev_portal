from django.test import TestCase
from django.urls import reverse_lazy

from apps.clients.tests.factories import ClientFactory

from apps.clients_requests.tests.factories import ClientsRequestFactory
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class ClientViewTest(CustomViewTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_client_1 = UserFactory(
                fio='Иванов Иван Иванович',
                role=UserRole.CLIENT,
                is_staff=False,
            )
        cls.client_1 = ClientFactory(
            user=cls.user_client_1,
            inn='1234567890',
            name='ИП Иванов Иван Иванович',
        )
        cls.user_admin = UserFactory(
            fio='Admin Admin Admin',
            role=UserRole.ADMIN,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        cls.clients_request = ClientsRequestFactory(
            title='title1',
            content='content1',
            author=cls.client_1,
        )

    @classmethod
    def setUpTestData(cls):
        # Create 33 clients for pagination tests
        number_of_clients = 33

        for client_id in range(number_of_clients):
            ClientFactory(
                inn=str(client_id).zfill(10),
                name=client_id,
            )

    def setUp(self) -> None:
        super().setUp()

    def test_list_01_url_exists_at_desired_location(self):
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 302)

        # get redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_list_02_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('clients:list'))
        self.assertEqual(response.status_code, 302)

        # get redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_list_03_uses_correct_template(self):
        response = self.client.get(reverse_lazy('clients:list'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_05(self):

        self.auth_user(self.user_admin)

        response = self.client.get(reverse_lazy('clients:list') + '?page=2')
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
