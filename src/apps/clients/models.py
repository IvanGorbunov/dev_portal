from django.db import models, transaction
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _
from rest_framework.utils import json

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from utils.models import CreateModelMixin

from .choices import ClientsStatus
from ..products.models import Product
from ..products.serializers import ProductListSerializer
from ..users.models import User


class Client(ChangeloggableMixin, CreateModelMixin, models.Model):
    """ Модель агентов """
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='client', blank=True, null=True, on_delete=models.PROTECT)
    inn = models.CharField('ИНН Агента', null=False, max_length=12, unique=True)
    name = models.CharField('Наименование Агента', null=False, max_length=350)
    phone = models.CharField('Телефон Агента', null=False, max_length=20)
    email = models.EmailField('e-mail', null=False, max_length=100)
    status = models.CharField(_('Status'), max_length=20, choices=ClientsStatus.CHOICES, default=ClientsStatus.NEW)
    is_delete = models.BooleanField(_('Deleted'), default=False)

    products = models.ManyToManyField(Product, verbose_name=_('Products'), related_name='clients', blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = [
            '-id',
        ]

    def __str__(self) -> str:
        return f'Client: {self.name} - {self.inn}'

    def destroy(self):
        self.is_delete = True
        self.save()


post_save.connect(journal_save_handler, sender=Client)
post_delete.connect(journal_delete_handler, sender=Client)
