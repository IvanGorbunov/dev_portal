from django.utils.translation import gettext_lazy as _


class ActionsType:
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    ITEMS = [
        CREATE,
        UPDATE,
        DELETE,
    ]

    CHOICES = (
        (CREATE, _('Создание')),
        (UPDATE, _('Изменение')),
        (DELETE, _('Удаление')),
    )
