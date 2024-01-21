import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


LOG = logging.getLogger(__name__)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'fio',
        'email',
        'get_fio',
        'phone',
        'role',
        'is_active'
    )
    search_fields = (
        'fio',
        'email',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': ('email', 'password')
            }
        ),
        (
            _('Personal info'), {
                'fields': ('fio', 'phone', 'role')
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
        'email',
        'fio',
    )
    list_filter = (
        'role',
        'is_active',
    )
    ordering = (
        'email',
    )
    # actions = (
    #     'approve_registration',
    #     'reject_registration',
    # )
    #
    # @admin.action(description=_('Approve registration for selected users'))
    # def approve_registration(self, request, queryset):
    #     for user in queryset:
    #         user.is_active = True
    #         user.is_need_new_password = True
    #         if user.is_rejected:
    #             user.is_rejected = False
    #         new_pasword = PasswordGenerator().generate()
    #         user.set_password(new_pasword)
    #         user.save()
    #         LOG.info(f'New password generated: {user.email} - {new_pasword}')
    #         email_body = f'Добрый день, {user.fio}!\n' \
    #                      f'Завершен процесс регистрации на сайте "ЛК ПапаФинанс".\n ' \
    #                      f'Временный пароль для входа: {new_pasword}\n ' \
    #                      f'Необходимо установить новый пароль при входе.\n '
    #
    #         Sender.send_mails_to_new_agent_verify(users_email=user.email, message=email_body)
    #
    # @admin.action(description=_('Reject registration for selected users'))
    # def reject_registration(self, request, queryset):
    #     for user in queryset:
    #         user.is_active = False
    #         user.is_rejected = True
    #         user.save()
    #         email_body = f'Добрый день, {user.fio}!\n' \
    #                      f'Администрацией отклонена регистрация на сайте "ЛК ПапаФинанс".\n '
    #
    #         Sender.send_mails_to_new_agent_verify(users_email=user.email, message=email_body)
