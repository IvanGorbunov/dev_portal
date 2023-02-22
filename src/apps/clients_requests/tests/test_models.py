from django.test import TestCase

from apps.clients.tests.factories import AgentFactory
from apps.clients_requests.choices import StatusAgentsRequest
from apps.clients_requests.models import AgentsRequest, AgentsRequestHistory
from apps.clients_requests.tests.factories import AgentsRequestFactory
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class TestModels(CustomViewTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_agent_1 = UserFactory(
                username='IvanovII',
                fio='Иванов Иван Иванович',
                role=UserRole.AGENT,
                is_staff=False,
            )
        cls.agent_1 = AgentFactory(
            user=cls.user_agent_1,
            inn='1234567890',
            name='ИП Иванов Иван Иванович'

        )
        cls.user_admin = UserFactory(
            username='AdminAA',
            fio='Admin Admin Admin',
            role=UserRole.ADMIN,
            is_staff=True,
        )
        cls.clients_request = AgentsRequestFactory(
            title='title1',
            content='content1',
            author=cls.agent_1,
        )  # type: AgentsRequest

    def test_clients_request_status(self):

        # проверим статус по умолчанию
        request = AgentsRequest.objects.filter(author=self.agent_1).first()
        self.assertEquals(request.status, StatusAgentsRequest.NEW)

        # проверим статус в истории по умолчанию
        history = AgentsRequestHistory.objects.filter(clients_request=self.clients_request).order_by('-date').first()
        self.assertEquals(history.status, StatusAgentsRequest.NEW)

        # проверим установку нового статуса в истории
        self.clients_request.status = StatusAgentsRequest.PENDING
        self.clients_request.save()

        history = AgentsRequestHistory.objects.filter(agents_request=self.agents_request).order_by('-date').first()
        self.assertEquals(history.status, StatusAgentsRequest.PENDING)

    def test_agents_request_delete(self):
        self.agents_request.destroy()
        request = AgentsRequest.objects.filter(pk=self.agents_request.id).first()
        self.assertEquals(request.is_delete, True)
