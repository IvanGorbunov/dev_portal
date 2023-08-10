from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _

from rest_framework.reverse import reverse_lazy

from .forms import ArticleCreationForm
from .models import Article
from utils.views import ContextDataMixin, DataMixin


class ArticleView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    queryset = Article.objects.filter(is_delete=False)
    context_object_name = 'articles'
    template_name = 'articles/articles_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = _('List of articles')

        return dict(list(context.items()) + list(c_def.items()))


class ArticleUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    queryset = Article.objects.filter(is_delete=False)
    template_name = 'articles/articles_item.html'
    success_url = reverse_lazy('articles:list')
    form_class = ArticleCreationForm

    def get_queryset(self):
        qs = super().get_queryset()  # type: QerySet
        qs = qs.select_related('author')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = _('Article')

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

