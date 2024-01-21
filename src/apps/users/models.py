from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import UserRole


class UserManager(BaseUserManager):
    """ Define a model manager for User model with no username field. """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a regular User with the given email and password. """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password. """
        if password is None:
            raise TypeError(_('Password should not be none'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ User`s model """

    email = models.EmailField(_('e-mail'), unique=True)
    phone = models.CharField(_('Phone'), max_length=35, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=350, blank=True, null=True)
    role = models.CharField(_('Role'), max_length=20, choices=UserRole.CHOICES, default=UserRole.CLIENT)
    is_staff = models.BooleanField(_('Stuff'), default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ['-id']

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.original_password = self.password

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self._password_has_been_changed():
            UserPasswordHistory.remember_password(self)

    def _password_has_been_changed(self):
        return self.original_password != self.password

    def get_field_name(self):
        return f'{self.fio} ({self.username})'

    def get_fio(self):
        return self.fio

    def get_phone(self):
        return self.phone

    def is_role_admin_or_super_admin(self):
        """Is admin or superadmin"""
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]

    def is_role_super_admin(self):
        """Is superadmin"""
        return self.role == UserRole.SUPER_ADMIN

    def is_role_admin(self):
        """Is admin"""
        return self.role == UserRole.ADMIN

    def is_role_client(self):
        """Is client"""
        return self.role == UserRole.CLIENT

    def is_role_staff(self):
        """Is staff"""
        return self.role == UserRole.STAFF

    def is_role_staff_or_admin(self):
        """Is admin or staff"""
        return self.role in UserRole.STUFF_ITEMS


class UserPasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_pass = models.CharField(max_length=128)
    pass_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def remember_password(cls, user):
        cls(user=user, old_pass=user.password).save()


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
