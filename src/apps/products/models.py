from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cte import CTEManager


class Category(models.Model):
    """ Model of Categories """
    name = models.CharField(_('Category`s name'), null=False, max_length=350, default='')
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), related_name='categories', blank=True, null=True, on_delete=models.CASCADE)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    objects: CTEManager = CTEManager()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    """ Model of products """
    name = models.CharField(_('Product`s name'), null=False, max_length=350)
    description = models.TextField(_('Description'), blank=True, null=True)

    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products',
                                 on_delete=models.PROTECT, blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self) -> str:
        return f'{self.name}'
