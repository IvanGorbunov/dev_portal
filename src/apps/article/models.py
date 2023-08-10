import logging

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .choices import ArticleType, ArticleStatus, AccessType, ScoreType
from ..users.models import User
from utils.models import DateModelMixin, CounterQuerySetMixin, CreateModelMixin

LOG = logging.getLogger(__name__)


class ArticleQuerySet(CounterQuerySetMixin):
    def filter_permission(self, user):
        """
        Rule Filter
        Example: queryset.filter_permission(request.user)

        1) For admin skip all checks
        2) For developers get access to types: ALL, DEVELOPERS
        3) For clients get access to types: ALL

        """
        if user.is_role_admin_or_super_admin():
            return self

        if user.is_role_staff():
            return self.filter(access_type__in=[AccessType.ALL, AccessType.DEVELOPERS, ])

        return self.filter(access_type__in=AccessType.ALL)


class Article(DateModelMixin, models.Model):
    """
    Article
    """
    title = models.CharField(_('Title'), max_length=250)
    is_delete = models.BooleanField(_('Deleted'), default=False)
    is_secret = models.BooleanField(_('Trade secret'), default=False)
    content_html = models.TextField(_('Description'))
    type = models.CharField(_('Type'), max_length=30, choices=ArticleType.CHOICES, default=ArticleType.ARTICLE)
    status = models.CharField(_('Status'), max_length=30, choices=ArticleStatus.CHOICES, default=ArticleStatus.DRAFT)
    access_type = models.CharField(_('Access type'), max_length=30, choices=AccessType.CHOICES, blank=True, null=True)

    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='articles', on_delete=models.PROTECT)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title

    def destroy(self):
        # set deleted
        self.is_delete = True
        self.save()

    def is_project(self):
        """
        Type: 'Project'
        """
        return self.type == ArticleType.PROJECT

    def is_draft(self):
        """
        Status: 'Draft'
        """
        return self.status == ArticleStatus.DRAFT

    def is_on_actualization(self):
        """
        Status: 'On actualisation'
        """
        return self.status == ArticleStatus.ON_ACTUALIZATION

    def add_view(self, user):
        try:
            ArticleView.objects.get_or_create(user=user, article=self)
        except Exception as ex:
            LOG.exception(f'Failed to create ArticleView: {ex}')


class ArticleView(CreateModelMixin, models.Model):
    """
    Count of views
    """
    article = models.ForeignKey(Article, verbose_name=_('Article'), related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='article_views', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Article view'
        verbose_name_plural = 'Articles views'
        unique_together = (('user', 'article'),)


# region Score

class ArticleScore(models.Model):
    """
    Count of score
    """
    article = models.ForeignKey(Article, verbose_name=_('Article'), related_name='score', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='article_scores', on_delete=models.CASCADE)

    type = models.CharField(_('Type'), max_length=30, choices=ScoreType.CHOICES, default=ScoreType.POINTS)

    value_points = models.IntegerField(_('Points'), null=True)
    value_duration = models.DurationField(_('Duration'), null=True)

    class Meta:
        verbose_name = 'Article points'
        verbose_name_plural = 'Articles points'

        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_valuematches_type',
                check=(
                        Q(type=ScoreType.POINTS, value_points__isnull=False, value_duration__isnull=True) |
                        Q(type=ScoreType.DURATION, value_points__isnull=True, value_duration__isnull=False)
                )
            ),
        ]


class ArticlePointScoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=ScoreType.POINTS)


class ArticlePointScore(ArticleScore):
    objects = ArticlePointScoreManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ScoreType.POINTS


class ArticleDurationScoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=ScoreType.DURATION)


class ArticleDurationScore(ArticleScore):
    objects = ArticleDurationScoreManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ScoreType.DURATION

# endregion Score
