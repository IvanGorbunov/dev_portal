from django.utils.translation import gettext_lazy as _


class StatusClientsRequest:
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    CANCELED = 'canceled'
    PENDING = 'pending'
    NEW = 'new'

    ITEMS = [
        COMPLETED,
        IN_PROGRESS,
        CANCELED,
        PENDING,
        NEW,
    ]

    CHOICES = (
        (COMPLETED, _('Completed')),
        (IN_PROGRESS, _('In progress')),
        (CANCELED, _('Canceled')),
        (PENDING, _('Pending')),
        (NEW, _('New')),
    )


class ClientsRequestAttachmentType:
    MEDIA = 'media'
    ATTACHMENT = 'attachment'

    ITEMS = [
        MEDIA,
        ATTACHMENT
    ]

    CHOICES = (
        (MEDIA, 'Медиа'),
        (ATTACHMENT, 'Приложение'),
    )
