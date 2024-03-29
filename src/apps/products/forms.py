from django import forms

from .models import Product


class ProductItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class CategoryItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
