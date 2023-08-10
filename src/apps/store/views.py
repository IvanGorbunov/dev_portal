from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView

from rest_framework.reverse import reverse_lazy, reverse

from apps.store.forms import PriceListItemForm
from apps.store.models import PriceList
from utils.views import DataMixin, ContextDataMixin


class PriceListView(LoginRequiredMixin, DataMixin, ContextDataMixin, ListView):
    model = PriceList
    context_object_name = 'pricelists'
    template_name = 'store/pricelist_list.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_delete=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список прайс-листов'

        return dict(list(context.items()) + list(c_def.items()))


class PriceListUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = PriceList
    form_class = PriceListItemForm
    template_name = 'store/pricelist_item.html'
    success_url = reverse_lazy('store:pricelist-list')
    context_object_name = 'pricelist'


class PriceListDownloadView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = PriceList
    form_class = PriceListItemForm
    template_name = 'store/pricelist_item.html'
    success_url = reverse_lazy('store:pricelist-list')
    context_object_name = 'pricelist'
    http_method_names = [
        "get",
    ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        price = PriceList.objects.get(pk=pk)
        price.counter += 1
        price.save()
        return redirect(price.file.url)
