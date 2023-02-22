from django import forms
from django.utils.translation import gettext_lazy as _

from apps.clients_requests.models import ClientsRequest


class ClientsRequestItemForm(forms.ModelForm):
    attachments = forms.FileField(label='Вложения:', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ClientsRequest
        fields = '__all__'
