
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from apps.products.models import Product


class ProductFactory(DjangoModelFactory):
    """
    Фабрика Продукта
    """
    class Meta:
        model = Product

    name = FuzzyText()
