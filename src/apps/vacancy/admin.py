from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from apps.vacancy.choices import VacancyStatus
from apps.vacancy.models import Vacancy, HR, TestProject, Position, Language, Country, Company, Currency


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = (
        'id',
        'position',
        'company',
        'hr',
        'salary',
        'salary_max',
        'currency',
        'language',
        'country',
        'status',
        'intensity',
        'resume_sent_dt',
        'interview_dt',
        'published_dt',
        'is_delete',
    )
    list_filter = (
        'status',
        'is_delete',
        'language',
        'country',
        'position',
        'company',
        'currency',
        'intensity',
    )
    search_fields = (
        'position',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'position',
    )
    fieldsets = (
        (
            _('Base info'), {
                'fields': (
                    'position',
                    'hr',
                    'country',
                    'company',
                    'language',
                    'intensity',
                )
            }
        ),
        (
            _('Salary'), {
                'fields': (
                    'salary',
                    'salary_max',
                    'currency',
                )
            }
        ),
        (
            _('Status info'), {
                'fields': (
                    'status',
                    'created_dt',
                    'published_dt',
                    'resume_sent_dt',
                    'interview_dt',
                    'is_delete',
                )
            }
        ),
        (
            _('Description'), {
                'fields': ('description', )
            }
        ),
        (
            _('Projects'), {
                'fields': ('test_projects',)
            }
        ),
    )
    readonly_fields = ('created_dt', )
    ordering = (
        '-id',
    )
    actions = (
        'set_status_old',
    )

    @admin.action(description=_('Set status - old'))
    def set_status_old(self, request, queryset):
        for i in queryset:
            i.status = VacancyStatus.OLD
            i.save()


@admin.register(HR)
class HRAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'telegram',
        'phone',
        'is_delete',
    )
    list_filter = (
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
    ordering = (
        'name',
    )


@admin.register(TestProject)
class TestProjectAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'start_dt',
        'finish_dt',
        'is_delete',
    )
    list_filter = (
        'is_delete',
        'status',
    )
    search_fields = (
        'name',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'name',
    )
    ordering = (
        'name',
    )


@admin.register(Position)
class PositionAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'full_name',
        'is_delete',
    )
    list_filter = (
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
    ordering = (
        'name',
    )


@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'language_level',
        'is_delete',
    )
    list_filter = (
        'is_delete',
        'language_level',
    )
    search_fields = (
        'name',
    )
    list_per_page = 25
    list_display_links = (
        'id',
        'name',
    )
    ordering = (
        'name',
    )


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_delete',
    )
    list_filter = (
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
    ordering = (
        'name',
    )


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'reference',
        'is_delete',
    )
    list_filter = (
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
    ordering = (
        'name',
    )


@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_delete',
    )
    list_filter = (
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
    ordering = (
        'name',
    )
