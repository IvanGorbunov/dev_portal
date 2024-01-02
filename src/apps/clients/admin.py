from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Client


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'inn',
        'user',
        'phone',
        'email',
        'status',
        'is_delete',
    )
    list_filter = (
        'status',
        'is_delete',
    )
    search_fields = (
        'name',
        'inn',
        'user',
        'phone',
        'email',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'name',
    )
    readonly_fields = ('created_at',)
