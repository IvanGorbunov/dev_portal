from apps.store.models import PriceList


def price_list(request):
    """Прайс лист"""
    price = PriceList.objects.filter(is_active=True)
    return {'price_list': price}
