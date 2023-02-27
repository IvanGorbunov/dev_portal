import string

import factory.fuzzy
from factory.django import DjangoModelFactory

from apps.clients.models import Client
from apps.users.tests.factories import UserFactory


class ClientFactory(DjangoModelFactory):
    """
    Фабрика Клиента
    """
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    inn = factory.fuzzy.FuzzyText(length=12, chars=string.digits)
    name = factory.fuzzy.FuzzyText(length=120)
    email = factory.fuzzy.FuzzyText(length=12, suffix='_a@yandex.ru')
