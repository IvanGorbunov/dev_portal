import logging

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin, confirm_action
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Article, ArticleView, ArticleScore


LOG = logging.getLogger(__name__)


@admin.register(Article)
class ArticleAdmin(ExtraButtonsMixin, ModelAdmin):
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

    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'})
    def delete_articles(self, request):
        def _action(request):
            LOG.info(f'Start deleting articles marked as deleted from admin-panel.')
            try:
                Article.delete_marked()
            except Exception as ex:
                LOG.error(f"Delete articles failed, error message: {ex}")

        return confirm_action(self, request, _action, "Confirm deleting articles  marked as deleted.",
                              "Successfully deleted articles.", )


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
