
class UserRole:
    ADMIN = 'admin'
    STAFF = 'staff'
    SUPER_ADMIN = 'super_admin'
    CLIENT = 'client'

    ITEMS = [
        ADMIN,
        STAFF,
        SUPER_ADMIN,
        CLIENT,
    ]

    STUFF_ITEMS = [
        ADMIN,
        STAFF,
        SUPER_ADMIN,
    ]

    CHOICES = (
        (ADMIN, 'Администратор портала'),
        (STAFF, 'Пользователь портала'),
        (SUPER_ADMIN, 'Суперадмин'),
        (CLIENT, 'Клиент'),
    )
