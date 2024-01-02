from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """ Модель продуктов """
    name = models.CharField(_('Product`s name'), null=False, max_length=350)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self) -> str:
        return f'{self.name}'
