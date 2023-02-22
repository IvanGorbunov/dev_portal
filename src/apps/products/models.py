from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """ Модель продуктов """
    name = models.CharField('Наименование продукта', null=False, max_length=350)
    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self) -> str:
        return f'Product: {self.name}'
