
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """
    Фабрика Пользователя
    """
    class Meta:
        model = User

    username = FuzzyText(length=12)
    email = FuzzyText(length=12, suffix='_a@yandex.ru')
    fio = FuzzyText(length=25)
