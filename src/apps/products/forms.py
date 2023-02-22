from django import forms

from apps.products.models import Product


class ProductItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
