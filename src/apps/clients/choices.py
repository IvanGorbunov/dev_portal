
class ClientsStatus:
    ACTIV = 'activ'
    NOT_ACTIV = 'not_activ'
    NEW = 'new'

    ITEMS = [
        ACTIV,
        NOT_ACTIV,
        NEW,
    ]

    CHOICES = (
        (ACTIV, 'Активен'),
        (NOT_ACTIV, 'Не активен'),
        (NEW, 'Новый'),
    )
