from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .choices import ClientsStatus
from .models import Client


class ClientCreationForm(forms.ModelForm):
    inn = forms.CharField(max_length=12)
    status = forms.CharField(max_length=20, empty_value=ClientsStatus.NEW)
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ClientCreationForm, self).__init__(*args, **kwargs)

    def clean_inn(self):
        form_inn = self.cleaned_data.get('inn')

        existing = Client.objects.filter(~Q(id=self.instance.id), inn=form_inn).exists()
        if existing:
            raise ValidationError(_('Such INN already exists.'))

        if len(form_inn) != 10 and len(form_inn) != 12:
            raise ValidationError(_('INN not fully specified.'))
        return form_inn
