from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    fio = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = '__all__'


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
        )


class RegisterForm(forms.Form):
    confirmation = forms.BooleanField(widget=forms.RadioSelect(attrs={"class": "form-control;"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control;"}))

    def clean_confirmation(self):
        if self.cleaned_data["confirmation"] is not True:
            raise ValidationError("You must confirm!")
