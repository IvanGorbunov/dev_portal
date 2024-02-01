from django.db.models import QuerySet, F, Value, IntegerField, TextField, Case, When, CharField
from django.db.models.functions import Concat
from django_cte import With

from apps.products.models import Category


def make_categories_cte(cte: With):
    # none-recursive: get root nodes
    qs = Category.objects
    qs = qs.values(
        'id',
        p=F('parent_id'),
        full_name=Case(
            When(name__isnull=True, then=Value('')),
            default=F('name'),
            output_field=CharField(),
        ),
        depth=Value(1, output_field=IntegerField()),
    )
    qs = qs.union(
        # recursive union: get descendance
        cte.join(Category, parent=cte.col.id).values(
            'id',
            p=cte.col.p,
            full_name=Concat(cte.col.full_name, Value('/'), F('name'), output_field=TextField()),
            depth=cte.col.depth + Value(1, output_field=IntegerField()),
        ),
        all=True,
    )
    return qs


def get_root_categories_selector(*, filters=None) -> QuerySet[Category]:
    # TODO: Make filters correctly
    filters = filters or {}

    cte = With.recursive(make_categories_cte)
    qs = cte.join(
        Category.objects.all(),
        id=cte.col.id,
    )

    qs = qs.annotate(
        full_name=cte.col.full_name,
        depth=cte.col.depth,
        p=cte.col.p,
    )
    qs = qs.filter(**filters)
    qs = qs.filter(p__isnull=True)
    qs = qs.filter(**filters)
    qs = qs.with_cte(cte).order_by(
        'depth',
    )
    return qs
