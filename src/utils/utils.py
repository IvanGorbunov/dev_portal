from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now as tz_now


def generate_uniq_code():
    return str(tz_now().timestamp()).replace('.', '')


def model_to_dict(obj, exclude_models=['AutoField', 'ForeignKey', 'OneToOneField']):
    tree = {}
    for field_name in obj._meta.get_all_field_names():
        try:
            field = getattr(obj, field_name)
        except ObjectDoesNotExist:
            continue

        if field.__class__.__name__ in ['RelatedManager', 'ManyRelatedManager']:
            if field.model.__name__ in exclude_models:
                continue

            if field.__class__.__name__ == 'ManyRelatedManager':
                exclude_models.append(obj.__class__.__name__)
            subtree = []
            for related_obj in getattr(obj, field_name).all():
                value = model_to_dict(related_obj, exclude_models=exclude_models)
                if value:
                    subtree.append(value)
            if subtree:
                tree[field_name] = subtree

            continue

        field = obj._meta.get_field_by_name(field_name)[0]
        if field.__class__.__name__ in exclude_models:
            continue

        if field.__class__.__name__ == 'RelatedObject':
            exclude_models.append(field.model.__name__)
            tree[field_name] = model_to_dict(getattr(obj, field_name), exclude_models=exclude_models)
            continue

        value = getattr(obj, field_name)
        if value:
            tree[field_name] = value

    return tree
