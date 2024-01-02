from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .choices import ArticleStatus
from .models import Article


class ArticleCreationForm(forms.ModelForm):
    status = forms.CharField(max_length=20, empty_value=ArticleStatus.DRAFT)

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('user', None)
        super(ArticleCreationForm, self).__init__(*args, **kwargs)
