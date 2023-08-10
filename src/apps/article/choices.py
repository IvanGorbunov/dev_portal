from django.utils.translation import gettext_lazy as _


class LikeType:
    """
    Type of the like
    """
    LIKE = 'like'
    DISLIKE = 'dislike'

    ITEMS = [
        LIKE,
        DISLIKE,
    ]

    CHOICES = (
        (LIKE, _('Like')),
        (DISLIKE, _('Dislike')),
    )


class ArticleType:
    """
    Type of the article
    """
    ARTICLE = 'article'
    PROJECT = 'project'

    ITEMS = (
        ARTICLE,
        PROJECT,
    )

    CHOICES = (
        (ARTICLE, _('Article')),
        (PROJECT, _('Project')),
    )


class ArticleStatus:
    """
    Statuses of the article
    """
    DRAFT = 'draft'
    ON_APPROVAL = 'on_approval'
    REJECTED = 'rejected'
    AGREED = 'agreed'
    PUBLISHED = 'published'
    ON_REVISION = 'on_revision'
    ON_ACTUALIZATION = 'on_actualization'

    ITEMS = (
        DRAFT,
        ON_APPROVAL,
        REJECTED,
        AGREED,
        PUBLISHED,
        ON_REVISION,
        ON_ACTUALIZATION,
    )

    CHOICES = (
        (DRAFT, _('Draft')),
        (ON_APPROVAL, _('On approval')),
        (REJECTED, _('Rejected')),
        (AGREED, _('Agreed')),
        (PUBLISHED, _('Published')),
        (ON_ACTUALIZATION, _('On actualisation')),
    )


class AccessType:
    """
    Type of the access
    """
    ALL = 'all'
    DEVELOPERS = 'developers'
    ADMINS = 'administrators'


    ITEMS = [
        ALL,
        DEVELOPERS,
        ADMINS,
    ]

    CHOICES = (
        (ALL, _('All')),
        (DEVELOPERS, _('Developers')),
        (ADMINS, _('Administrators')),
    )


class ArticleAttachmentType:
    MEDIA = 'media'
    ATTACHMENT = 'attachment'

    ITEMS = [
        MEDIA,
        ATTACHMENT
    ]

    CHOICES = (
        (MEDIA, _('Media')),
        (ATTACHMENT, _('Attachment')),
    )


class ScoreType:
    POINTS = 'points'
    DURATION = 'duration'

    ITEMS = [
        POINTS,
        DURATION,
    ]

    CHOICES = (
        (POINTS, _('Points')),
        (DURATION, _('Duration')),
    )
