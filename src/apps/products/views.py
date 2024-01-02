from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from rest_framework.reverse import reverse_lazy

from .forms import ProductItemForm
from .models import Product
from utils.views import DataMixin, ContextDataMixin


class ProductView(LoginRequiredMixin, DataMixin, ContextDataMixin, ListView):
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список продуктов'

        return dict(list(context.items()) + list(c_def.items()))


class ProductUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    template_name = 'products/product_item.html'
    success_url = reverse_lazy('products:list')
    model = Product
    form_class = ProductItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукт'

        c_def = super().get_default_context_data()

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        if request.user.is_role_client():
            return render(request, 'not_allowed.html')
        return super().post(request, *args, **kwargs)
