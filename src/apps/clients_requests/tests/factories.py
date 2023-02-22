import string

import factory.fuzzy
from factory.django import DjangoModelFactory

from apps.agents.tests.factories import AgentFactory
from apps.agents_requests.models import AgentsRequest
from apps.users.tests.factories import UserFactory


class AgentsRequestFactory(DjangoModelFactory):
    """
    Фабрика Агентской заявки
    """
    class Meta:
        model = AgentsRequest

    title = factory.fuzzy.FuzzyText(length=255, chars=string.digits)
    content = factory.fuzzy.FuzzyText(length=255)

    author = factory.SubFactory(AgentFactory)
