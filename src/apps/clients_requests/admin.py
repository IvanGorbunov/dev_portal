import logging

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin, confirm_action
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.translation import gettext_lazy as _
from django_filters import DateRangeFilter

from .choices import StatusClientsRequest
from .models import ClientsRequest, ClientsRequestAttachment


LOG = logging.getLogger(__name__)


class ClientsRequestAttachmentInline(TabularInline):
    verbose_name_plural = _('Attachment of the request')
    model = ClientsRequestAttachment
    extra = 0


@admin.register(ClientsRequest)
class ClientsRequestAdmin(ExtraButtonsMixin, ModelAdmin):
    inlines = (
        ClientsRequestAttachmentInline,
    )
    list_display = (
        'id',
        'title',
        'author',
        'created_at',
        'status',
        'is_delete',
    )
    search_fields = (
        'title',
        'author',
    )
    list_filter = (
        'status',
        'created_at',
        'is_delete',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'title',
    )
    readonly_fields = ('created_at', 'updated_at',)
    actions = (
        'mark_as_deleted',
        'mark_as_completed',
        'mark_as_in_progress',
        'mark_as_canceled',
        'mark_as_pending',
    )

    @admin.action(description=_('Client requests are marked as deleted'))
    def mark_as_deleted(self, request, queryset):
        for item in queryset:
            item.destroy()

    @admin.action(description=_('Client requests are marked as completed'))
    def mark_as_completed(self, request, queryset):
        for item in queryset:
            item.status = StatusClientsRequest.COMPLETED
            item.save()

    @admin.action(description=_('Client requests are marked as in progress'))
    def mark_as_in_progress(self, request, queryset):
        for item in queryset:
            item.status = StatusClientsRequest.IN_PROGRESS
            item.save()

    @admin.action(description=_('Client requests are marked as canceled'))
    def mark_as_canceled(self, request, queryset):
        for item in queryset:
            item.status = StatusClientsRequest.CANCELED
            item.save()

    @admin.action(description=_('Client requests are marked as pending'))
    def mark_as_pending(self, request, queryset):
        for item in queryset:
            item.status = StatusClientsRequest.PENDING
            item.save()

    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'})
    def delete_clients_requests(self, request):
        def _action(request):
            LOG.info(f'Start deleting client`s requests marked as deleted from admin-panel.')
            try:
                ClientsRequest.delete_marked()
            except Exception as ex:
                LOG.error(f"Delete client`s requests failed, error message: {ex}")

        return confirm_action(self, request, _action, "Confirm deleting client`s requests  marked as deleted.",
                              "Successfully deleted client`s requests.", )


@admin.register(ClientsRequestAttachment)
class ClientsRequestAttachmentAdmin(ModelAdmin):
    list_display = (
        'id',
        'order_num',
        'clients_request',
        'name',
        'type',
    )
    list_filter = (
        'type',
    )
    search_fields = (
        'clients_request',
        'name',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'clients_request',
        'name',
    )
