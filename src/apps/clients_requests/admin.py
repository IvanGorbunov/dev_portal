from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.translation import gettext_lazy as _
from django_filters import DateRangeFilter

from .models import ClientsRequest, ClientsRequestAttachment


class ClientsRequestAttachmentInline(TabularInline):
    verbose_name_plural = _('Attachment of the request')
    model = ClientsRequestAttachment
    extra = 0


@admin.register(ClientsRequest)
class ClientsRequestAdmin(ModelAdmin):
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
