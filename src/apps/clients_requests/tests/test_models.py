from django.test import TestCase

from apps.clients.tests.factories import ClientFactory
from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.models import ClientsRequest, ClientsRequestHistory
from apps.clients_requests.tests.factories import ClientsRequestFactory
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class TestModels(CustomViewTestCase):

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
            name='ИП Иванов Иван Иванович'

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
        )  # type: clientsRequest

    def test_clients_request_status(self):

        # проверим статус по умолчанию
        request = ClientsRequest.objects.filter(author=self.client_1).first()
        self.assertEquals(request.status, StatusClientsRequest.NEW)

        # проверим статус в истории по умолчанию
        history = ClientsRequestHistory.objects.filter(clients_request=self.clients_request).order_by('-date').first()
        self.assertEquals(history.status, StatusClientsRequest.NEW)

        # проверим установку нового статуса в истории
        self.clients_request.status = StatusClientsRequest.PENDING
        self.clients_request.save()

        history = ClientsRequestHistory.objects.filter(clients_request=self.clients_request).order_by('-date').first()
        self.assertEquals(history.status, StatusClientsRequest.PENDING)

    def test_clients_request_delete(self):
        self.clients_request.destroy()
        request = ClientsRequest.objects.filter(pk=self.clients_request.id).first()
        self.assertEquals(request.is_delete, True)
