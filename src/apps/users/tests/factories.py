from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """
    Фабрика Пользователя
    """

    username = FuzzyText(length=12)
    password = PostGenerationMethodCall('set_password', 'adm1n')
    email = FuzzyText(length=12, suffix='_a@example.com')
    fio = FuzzyText(length=25)

    class Meta:
        model = User
