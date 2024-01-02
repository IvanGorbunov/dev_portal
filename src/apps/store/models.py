from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import DateModelMixin


class PriceList(DateModelMixin, models.Model):
    """Модель прайс листа"""
    title = models.CharField(_('Price`s name'), max_length=250)
    file = models.FileField(_('File'), upload_to='price_list/%y/%m/%d/')
    counter = models.PositiveIntegerField(_('Number of downloads'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    is_delete = models.BooleanField(_('Deleted'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Прайс лист')
        verbose_name_plural = _('Прайс листы')
        ordering = ['-created_at']
