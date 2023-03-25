from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product


@admin.register(Product)
class clientAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_delete',
    )
    search_fields = (
        'name',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'name',
    )
