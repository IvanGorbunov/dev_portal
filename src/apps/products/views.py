from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from rest_framework.reverse import reverse_lazy

from .forms import ProductItemForm, CategoryItemForm
from .models import Product, Category
from utils.views import DataMixin, ContextDataMixin
from .selectors import get_root_categories_selector


class ProductView(LoginRequiredMixin, DataMixin, ContextDataMixin, ListView):
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = _('Products list')

        return dict(list(context.items()) + list(c_def.items()))


class ProductUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Product
    form_class = ProductItemForm
    template_name = 'products/product_item.html'
    success_url = reverse_lazy('products:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Product')

        c_def = super().get_default_context_data()

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        if request.user.is_role_client():
            return render(request, 'not_allowed.html')
        return super().post(request, *args, **kwargs)


class CategoryView(LoginRequiredMixin, DataMixin, ContextDataMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'products/categories_list.html'

    def get_queryset(self):
        return get_root_categories_selector()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = _('Categories list')

        return dict(list(context.items()) + list(c_def.items()))


class CategoryUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Category
    form_class = CategoryItemForm
    template_name = 'products/category_item.html'
    success_url = reverse_lazy('products:categories-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Category')

        c_def = super().get_default_context_data()

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        if request.user.is_role_client():
            return render(request, 'not_allowed.html')
        return super().post(request, *args, **kwargs)
