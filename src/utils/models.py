from django.db import models
from django.db.models import Q, Exists, OuterRef, Subquery, Count
from django.utils.translation import gettext_lazy as _


class CreateModelMixin(models.Model):

    created_at = models.DateTimeField(_('Created'), db_index=True,  auto_now_add=True)

    class Meta:
        abstract = True


class DateModelMixin(CreateModelMixin, models.Model):

    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        abstract = True


class SubqueryAggregate:
    """
    Класс для агрегаций в подзапросах
    """
    def __init__(self, sub_model, aggregate, name, filters=None) -> None:
        self.sub_model = sub_model
        self.aggregate = aggregate
        self.name = name
        self.filters = filters or Q()
        super().__init__()

    def subquery(self):
        """
        # todo: Надо попробовать переделать на .values(annotate_value=self.aggregate('pk'))
        """
        query = self.sub_model.objects.filter(
            self.filters,
            **{self.name: OuterRef('pk')},
        ).values(self.name).annotate(annotate_value=self.aggregate('pk')).values('annotate_value')
        return Subquery(query)


class CounterQuerySetMixin(models.QuerySet):

    def annotate_likes_count(self):
        """
        Аннотация количества лойков
        """
        field = self.model.likes.field
        sub_class = SubqueryAggregate(field.model, Count, field.name, Q(type=LikeType.LIKE))
        return self.annotate(likes_count=sub_class.subquery())

    def annotate_dislikes_count(self):
        """
        Аннотация количества дизлайков
        """
        field = self.model.likes.field
        sub_class = SubqueryAggregate(field.model, Count, field.name, Q(type=LikeType.DISLIKE))
        return self.annotate(dislikes_count=sub_class.subquery())

    def annotate_my_like(self, user):
        """
        Мой лайк
        """
        field = self.model.likes.field
        my_like_qs = field.model.objects.filter(**{field.name: OuterRef('pk'), 'user': user}).only_likes()
        return self.annotate(my_like=Exists(my_like_qs))

    def annotate_my_dislike(self, user):
        """
        Мой дизлайк
        """
        field = self.model.likes.field
        my_like_qs = field.model.objects.filter(**{field.name: OuterRef('pk'), 'user': user}).only_dislikes()
        return self.annotate(my_dislike=Exists(my_like_qs))

    def annotate_views_count(self):
        field = self.model.views.field
        sub_class = SubqueryAggregate(field.model, Count, field.name)
        return self.annotate(views_count=sub_class.subquery())

    def annotate_comments_count(self):
        """
        Анотация количества комментариев
        """
        field = self.model.comments.field
        sub_class = SubqueryAggregate(field.model, Count, field.name)
        return self.annotate(comments_count=sub_class.subquery())

    def annotate_my_favourite(self, user):
        favourite_model = self.model.favourites.through
        model_name = self.model._meta.model_name
        my_favourite_qs = favourite_model.objects.filter(**{model_name: OuterRef('pk'), 'user_id': user.id})
        return self.annotate(my_favourite=Exists(my_favourite_qs))
