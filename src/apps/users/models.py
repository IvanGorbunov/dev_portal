from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import UserRole


class User(AbstractUser):
    """ Модель пользователей """
    email = models.EmailField(_('e-mail'), blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=35, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=350, blank=True, null=True)
    role = models.CharField(_('Role'), max_length=20, choices=UserRole.CHOICES, default=UserRole.CLIENT)
    is_staff = models.BooleanField(_('Stuff'), default=False)

    first_name = None
    last_name = None

    class Meta(AbstractUser.Meta):
        ordering = ['-id']

    def get_field_name(self):
        return f'{self.fio} ({self.username})'

    def get_fio(self):
        return self.fio

    def get_phone(self):
        return self.phone

    def is_role_admin_or_super_admin(self):
        """Администратор портала или суперадмин"""
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]

    def is_role_super_admin(self):
        """Суперадмин"""
        return self.role == UserRole.SUPER_ADMIN

    def is_role_admin(self):
        """Администратор портала"""
        return self.role == UserRole.ADMIN

    def is_role_client(self):
        """Клиент"""
        return self.role == UserRole.CLIENT

    def is_role_staff(self):
        """Сотрудник"""
        return self.role == UserRole.STAFF

    def is_role_staff_or_admin(self):
        """Администратор портала или сотрудник"""
        return self.role in UserRole.STUFF_ITEMS


class ClientManager(BaseUserManager):
    def get_queryset(self):
        qs = super(ClientManager, self).get_queryset()
        qs = qs.filter(role=UserRole.CLIENT)
        return qs

    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError(_('Email field is required !'))
        if not password:
            raise ValueError(_('Password is must !'))

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Client(User):
    class Meta:
        proxy = True

    objects = ClientManager()


class StuffManager(BaseUserManager):
    def get_queryset(self):
        return super(StuffManager, self).get_queryset().filter(role__in=UserRole.STUFF_ITEMS)


class Stuff(User):
    id = None

    objects = StuffManager()

    class Meta:
        proxy = True
