from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
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


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
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
