from django.test import TestCase
from django.urls import reverse_lazy

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

    def setUp(self) -> None:
        super().setUp()

    def test_list(self):
        self.auth_user(self.user_admin)
