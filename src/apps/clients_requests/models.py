from constrainedfilefield.fields import ConstrainedFileField
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from utils.models import DateModelMixin

from ..clients.models import Client
from ..clients_requests.choices import StatusClientsRequest, ClientsRequestAttachmentType
from ..products.models import Product
from ..users.models import User


class ClientsRequest(ChangeloggableMixin, DateModelMixin, models.Model):
    """ Модель клиентских заявок """
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Description'), blank=True, null=True)
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
            '-created_at',
        ]

    def __str__(self) -> str:
        return f'Clients request: {self.title} - {self.author}'

    def get_absolute_url(self):
        return reverse('clients_requests:clients-request-update', kwargs={'pk': self.pk})

    def destroy(self):
        self.is_delete = True
        self.save()

# region Attachments


class ClientsRequestAttachmentQuerySet(models.QuerySet):
    def media(self):
        return self.filter(type=ClientsRequestAttachmentType.MEDIA)

    def attachments(self):
        return self.filter(type=ClientsRequestAttachmentType.ATTACHMENT)


class ClientsRequestAttachment(models.Model):
    """ Модель: Вложение заявки """
    MAX_DOCUMENTS_NUM = 10
    MAX_SIZE_DOCUMENT = 1024 * 1024 * 10  # 10M

    order_num = models.IntegerField(_('Number'))
    clients_request = models.ForeignKey(ClientsRequest, verbose_name=_('Clients`s request'), related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100)
    format = models.CharField(_('File format'), max_length=15)
    about = models.TextField(_('Description'), blank=True, null=True)
    type = models.CharField(_('Attachment type'), max_length=15, choices=ClientsRequestAttachmentType.CHOICES, default=ClientsRequestAttachmentType.ATTACHMENT)
    attach_file = ConstrainedFileField(
        _('Attachment file'),
        null=True,
        blank=True,
        upload_to='attachments',
        content_types=(
            'application/pdf',
            'image/png',
            'image/jpg',
            'image/jpeg',
        ),
        max_upload_size=1024000
    )

    objects = ClientsRequestAttachmentQuerySet.as_manager()

    class Meta:
        verbose_name = _('Attachment of the request')
        verbose_name_plural = _('Attachments of the request')

# endregion


post_save.connect(journal_save_handler, sender=ClientsRequest)
post_delete.connect(journal_delete_handler, sender=ClientsRequest)
