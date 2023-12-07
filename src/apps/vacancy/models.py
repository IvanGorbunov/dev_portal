from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.vacancy.choices import TestProjectStatus, VacancyStatus, LanguageLevels


class HR(models.Model):
    name = models.CharField(max_length=150)
    telegram = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('HR')
        verbose_name_plural = _('HRs')

    def __str__(self):
        return f'{self.name}({self.telegram})'


class TestProject(models.Model):
    name = models.CharField(max_length=150)
    reference = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(_('Status'), max_length=30, choices=TestProjectStatus.CHOICES, default=TestProjectStatus.NEW)
    start_dt = models.DateTimeField(blank=True, null=True)
    finish_dt = models.DateTimeField(blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('TestProject')
        verbose_name_plural = _('TestProjects')

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=150)
    full_name = models.CharField(max_length=350, blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=150)
    language_level = models.CharField(_('Language level'), max_length=30, choices=LanguageLevels.CHOICES,
                                      default=LanguageLevels.A1)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return f'{self.name}({self.language_level})'

    def __repr__(self):
        return f'{self.name}({self.language_level})'


class Country(models.Model):
    name = models.CharField(max_length=250)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=250)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=250)
    reference = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    position = models.ForeignKey(Position, verbose_name=_('Position'), related_name='vacancies', on_delete=models.PROTECT)
    hr = models.ForeignKey(HR, verbose_name=_('HR'), related_name='vacancies', on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), related_name='vacancies', blank=True, null=True, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, verbose_name=_('Company'), related_name='vacancies', blank=True, null=True, on_delete=models.PROTECT)

    language = models.ForeignKey(Language, verbose_name=_('Language'), related_name='vacancies', blank=True, null=True, on_delete=models.PROTECT)

    salary = models.IntegerField(verbose_name=_('Salary'), blank=True, null=True)
    salary_max = models.IntegerField(verbose_name=_('Salary (max)'), blank=True, null=True)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), related_name='vacancies', blank=True, null=True,
                                 on_delete=models.PROTECT)

    test_projects = models.ManyToManyField(TestProject, verbose_name=_('Test projects'), related_name='vacancies', blank=True)

    status = models.CharField(_('Status'), max_length=30, choices=VacancyStatus.CHOICES, default=VacancyStatus.NEW)

    created_dt = models.DateTimeField(auto_now_add=True)
    resume_sent_dt = models.DateTimeField(blank=True, null=True)
    interview_dt = models.DateTimeField(blank=True, null=True)
    published_dt = models.DateTimeField(blank=True, null=True)

    is_delete = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')


