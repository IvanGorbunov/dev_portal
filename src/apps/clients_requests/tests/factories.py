import string

import factory.fuzzy
from factory.django import DjangoModelFactory

from apps.clients.tests.factories import ClientFactory
from apps.clients_requests.models import ClientsRequest
from apps.users.tests.factories import UserFactory


class ClientsRequestFactory(DjangoModelFactory):
    """
    Фабрика Агентской заявки
    """
    class Meta:
        model = ClientsRequest

    title = factory.fuzzy.FuzzyText(length=255, chars=string.digits)
    content = factory.fuzzy.FuzzyText(length=255)

    author = factory.SubFactory(ClientFactory)
