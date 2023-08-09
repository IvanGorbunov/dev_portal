from django.db import models
from django.utils.translation import gettext_lazy as _


class PriceList(models.Model):
    """Модель прайс листа"""
    title = models.CharField('Заголовок', max_length=250)
    file = models.FileField('Файл', upload_to='price_list/%y/%m/%d/')
    counter = models.PositiveIntegerField('Кол-во загрузок', default=0)
    is_active = models.BooleanField('Модерация', default=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Изменен', auto_now=True)
    is_delete = models.BooleanField(_('Deleted'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Прайс лист'
        verbose_name_plural = 'Прайс листы'
        ordering = ['-created']
