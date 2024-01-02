from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .choices import ActionsType


class ChangeLog(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Автор изменения'), on_delete=models.CASCADE, null=True)
    changed = models.DateTimeField(auto_now=True, verbose_name=_('Дата/время изменения'))
    model = models.CharField(max_length=255, verbose_name=_('Таблица'), null=True)
    record_id = models.IntegerField(verbose_name=_('ID записи'), null=True)
    action_on_model = models.CharField(choices=ActionsType.CHOICES, max_length=50, verbose_name=_('Действие'), null=True)
    data = models.JSONField(verbose_name=_('Изменяемые данные модели'), default=dict)
    ipaddress = models.CharField(max_length=15, verbose_name=_('IP адресс'), null=True)

    class Meta:
        verbose_name = _('Change log')
        verbose_name_plural = _('Change logs')
        ordering = ('changed',)

    def __str__(self):
        return f'{self.id}'

    @classmethod
    def add(cls, instance, user, ipaddress: str, action_on_model: ActionsType, data: dict, id: int = None) -> int:
        """Создание записи в журнале регистрации изменений"""
        log = ChangeLog.objects.get(id=id) if id else ChangeLog()
        log.model = instance.__class__.__name__
        log.record_id = instance.pk
        if user:
            log.user = user
        log.ipaddress = ipaddress
        log.action_on_model = action_on_model
        log.data = data
        log.save()
        return log.pk
