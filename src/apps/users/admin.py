from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'fio',
        'email',
        'get_fio',
        'phone',
        'role',
        'is_active'
    )
    search_fields = (
        'username',
        'fio',
        'email',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': ('username', 'password')
            }
        ),
        (
            _('Personal info'), {
                'fields': ('fio', 'email', 'phone', 'role')
            }
        ),
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
            }
        ),
        (
            _('Important dates'), {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )
    list_display_links = (
        'username',
        'fio',
    )
    list_filter = (
        'role',
        'is_active',
    )
