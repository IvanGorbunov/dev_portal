from django.db.models import F


def add_clients_fields(func: callable):
    """
    Add additional fields to querysets
    """
    def annotate_wrapper(*args, **kwargs):
        return func(*args, **kwargs).annotate(client_id=F('client__id')).annotate(client_name=F('client__name'))
    return annotate_wrapper


def add_users_context_data(context_local: dict = {}):
    """
    Create additional context for templates
    """
    def add_context_data(func: callable):
        def get_default_context_data_wrapper(*args, **kwargs):
            context = func(*args, **kwargs)     # get standard context
            context_default = args[0].get_default_context_data()    # get default context for current object
            return dict(list(context.items()) + list(context_default.items()) + list(context_local.items()))
        return get_default_context_data_wrapper
    return add_context_data
