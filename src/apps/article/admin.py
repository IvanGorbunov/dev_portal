from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Article, ArticleView, ArticleScore


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_delete',
        'is_secret',
        'type',
        'status',
        'access_type',
        'author',
    )
    list_filter = (
        'is_delete',
        'is_secret',
        'type',
        'status',
        'access_type',
    )
    search_fields = (
        'title',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'title',
    )


@admin.register(ArticleView)
class ArticleViewAdmin(ModelAdmin):
    list_display = (
        'id',
        'article',
        'user',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'article',
    )


@admin.register(ArticleScore)
class ArticleScoreAdmin(ModelAdmin):
    list_display = (
        'id',
        'article',
        'type',
        'value_points',
        'value_duration',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'article',
    )


