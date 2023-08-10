from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import PriceList


@admin.register(PriceList)
class PriceListAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'counter',
        'is_active',
        'created',
        'updated',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'is_active',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'title',
    )
