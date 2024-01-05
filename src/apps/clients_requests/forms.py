from django import forms
from django.utils.translation import gettext_lazy as _

from ..clients.models import Client
from .choices import StatusClientsRequest
from .models import ClientsRequest, ClientsRequestAttachment
from ..products.models import Product


class ClientsRequestItemForm(forms.ModelForm):
    attachments = forms.FileField(label=_('Attachments:'), widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
    status = forms.ChoiceField(label=_('Status'), widget=forms.HiddenInput(), choices=StatusClientsRequest.CHOICES, initial=StatusClientsRequest.NEW, required=False)
    is_delete = forms.BooleanField(label=_('Is delete'), widget=forms.HiddenInput(), initial=False, required=False)

    author = forms.ModelChoiceField(label=_('Author'), widget=forms.HiddenInput(), queryset=Client.objects.all())
    product = forms.ModelChoiceField(label=_('Product'), queryset=Product.objects.all())

    class Meta:
        model = ClientsRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        qs = Client.objects.filter(user=user)
        self.fields['author'].queryset = qs
        author = qs.first()
        self.fields['author'].initial = author
        self.fields['product'].queryset = author.products.all()


class ClientsRequestItemAdminForm(forms.ModelForm):
    attachments = forms.FileField(label=_('Attachments:'), widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
    status = forms.ChoiceField(label=_('Status'), choices=StatusClientsRequest.CHOICES, initial=StatusClientsRequest.NEW, required=False)
    is_delete = forms.BooleanField(label=_('Is delete'), initial=False, required=False)

    class Meta:
        model = ClientsRequest
        fields = '__all__'


class ClientsRequestAttachmentForm(forms.ModelForm):
    class Meta:
        model = ClientsRequestAttachment
        fields = ['attach_file']
