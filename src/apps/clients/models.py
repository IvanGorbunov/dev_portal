from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.utils import json

from apps.clients.choices import ClientsStatus
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from apps.users.models import User


class Client(models.Model):
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

    def __str__(self) -> str:
        return f'Client: {self.name} - {self.inn}'

    @transaction.atomic()
    def save(self, *args, **kwargs):
        is_adding = self._state.adding
        super().save(*args, **kwargs)
        if is_adding:
            serializer = ProductListSerializer(self.products, many=True)
            new_values = {
                'user_id': self.user_id,
                'inn': self.inn,
                'name': self.name,
                'phone': self.phone,
                'email': self.email,
                'status': self.status,
                'is_delete': self.is_delete,
                'products': serializer.data,
            }
            values = json.dumps(new_values)
            ClientsHistory.objects.create(client=self, values=values, user_id=self.user_id)

    @transaction.atomic()
    def update(self, instance, validated_data):

        client = super().update(instance, validated_data)

        serializer = ProductListSerializer(client.products, many=True)
        new_values = {
            'user_id': self.user_id,
            'inn': self.inn,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'status': self.status,
            'is_delete': self.is_delete,
            'products': serializer.data,
        }
        values = json.dumps(new_values)
        last_values = ClientsHistory.objects.filter(client=self).order_by('-date').values('values').first()
        if not last_values or last_values.get('values') != values:
            ClientsHistory.objects.create(client=self, values=values, user=self.get_request_user())

    def destroy(self):
        self.is_delete = True
        self.save()


class ClientsHistory(models.Model):
    """ История изменения агента"""
    client = models.ForeignKey('Client', verbose_name=_('Client'), related_name='client', on_delete=models.CASCADE)
    date = models.DateTimeField('Дата изменения', auto_now_add=True)
    values = models.TextField(_('Values'), blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='client_history_users', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = _('Clients history')
        verbose_name_plural = _('Clients history')
