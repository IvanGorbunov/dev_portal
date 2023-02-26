from django.test import TestCase
from django.urls import reverse_lazy

from apps.clients.tests.factories import ClientFactory
from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.models import ClientsRequest, ClientsRequestHistory
from apps.clients_requests.tests.factories import ClientsRequestFactory
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class AgentsRequestViewTest(CustomViewTestCase):

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
        cls.user_admin = UserFactory(
            username='AdminAA',
            fio='Admin Admin Admin',
            role=UserRole.ADMIN,
            is_staff=True,
        )
        cls.clients_request = ClientsRequestFactory(
            title='title1',
            content='content1',
            author=cls.client_1,
        )

    def setUp(self) -> None:
        super().setUp()

    @classmethod
    def setUpTestData(cls):
        # Create agent`s requests for pagination tests
        number_of_requests = 33

        for agent_id in range(number_of_requests):
            ClientsRequestFactory()

    def setUp(self) -> None:
        super().setUp()

    def test_list_01_url_exists_at_desired_location(self):
        response = self.client.get('/clients_requests/')
        self.assertEqual(response.status_code, 302)

        # get redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_list_02_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('clients_requests:list'))
        self.assertEqual(response.status_code, 302)

        # get redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_list_03_uses_correct_template(self):
        response = self.client.get(reverse_lazy('clients_requests:list'))
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_04(self):
        self.auth_user(self.user_admin)
        response = self.client.get(reverse_lazy('clients_requests:list') + '?page=2')
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
