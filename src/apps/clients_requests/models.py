from django.db import models, transaction
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.clients.models import Client
from apps.clients_requests.choices import StatusClientsRequest, ClientsRequestAttachmentType
from apps.products.models import Product
from apps.users.models import User


class ClientsRequest(models.Model):
    """ Модель агентских заявок """
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Description'), blank=True, null=True)
    create_dt = models.DateTimeField(_('Date of creation'), auto_now_add=True)
    update_dt = models.DateTimeField(_('Update date'), auto_now=True)
    status = models.CharField(_('Status'), max_length=20, choices=StatusClientsRequest.CHOICES, default=StatusClientsRequest.NEW)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    email = models.EmailField('e-mail', max_length=100, blank=True, null=True)

    author = models.ForeignKey(Client, verbose_name=_('Author'), related_name='clients_requests', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='clients_requests', on_delete=models.PROTECT, blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Clients request')
        verbose_name_plural = _('Clients requests')
        ordering = [
            '-create_dt',
        ]

    def __str__(self) -> str:
        return f'Clients request: {self.title} - {self.author}'

    def get_absolute_url(self):
        return reverse('clients_requests:clients-request-update', kwargs={'pk': self.pk})

    @transaction.atomic()
    def save(self, *args, **kwargs):
        self.update_dt = datetime.now()
        super().save(*args, **kwargs)
        last_status = ClientsRequestHistory.objects.filter(clients_request=self).order_by('-date').values('status').first()
        if not last_status or last_status.get('status') != self.status:
            ClientsRequestHistory.objects.create(clients_request=self, status=self.status)

    def destroy(self):
        self.is_delete = True
        self.save()


class ClientsRequestHistory(models.Model):
    """ История изменения заявки"""
    clients_request = models.ForeignKey('ClientsRequest', verbose_name=_('client'), related_name='client', on_delete=models.CASCADE)
    date = models.DateTimeField(_('Update date'), auto_now_add=True)
    status = models.CharField(_('Status'), max_length=20, choices=StatusClientsRequest.CHOICES, default=StatusClientsRequest.NEW)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='clients_requests_history_users', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = _('Clients`s request history')
        verbose_name_plural = _('Clients`s requests history')

# region Вложения


class ClientsRequestAttachmentQuerySet(models.QuerySet):
    def media(self):
        return self.filter(type=ClientsRequestAttachmentType.MEDIA)

    def attachments(self):
        return self.filter(type=ClientsRequestAttachmentType.ATTACHMENT)


class ClientsRequestAttachment(models.Model):
    """ Модель: Вложение заявки """
    order_num = models.IntegerField(_('Number'))
    clients_request = models.ForeignKey(ClientsRequest, verbose_name=_('Clients`s request'), related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100)
    format = models.CharField(_('File format'), max_length=15)
    about = models.TextField(_('Description'), blank=True, null=True)
    type = models.CharField(_('Attachment type'), max_length=15, choices=ClientsRequestAttachmentType.CHOICES, default=ClientsRequestAttachmentType.ATTACHMENT)
    file = models.FileField(_('Attachment file'), upload_to='attachments/', blank=True, null=True, default=None)

    objects = ClientsRequestAttachmentQuerySet.as_manager()

    class Meta:
        verbose_name = _('Attachment of the request')
        verbose_name_plural = _('Attachments of the request')

# endregion
