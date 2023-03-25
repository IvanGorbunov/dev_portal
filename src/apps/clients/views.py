from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView

from django.conf import settings
from rest_framework.reverse import reverse_lazy

from .choices import ClientsStatus
from .forms import ClientCreationForm
from .models import Client
from .services import send_letter
from utils.views import DataMixin, ContextDataMixin


class ClientsView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    queryset = Client.objects.filter(is_delete=False)
    context_object_name = 'clients'
    template_name = 'clients/clients_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список клиентов'
        c_def['statuses'] = [{'id': val[0], 'val': val[1]} for val in ClientsStatus.CHOICES]

        return dict(list(context.items()) + list(c_def.items()))


class ClientUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    queryset = Client.objects.filter(is_delete=False)
    template_name = 'clients/clients_profile.html'
    success_url = reverse_lazy('clients:list')
    form_class = ClientCreationForm

    def get_queryset(self):
        qs = super().get_queryset()  # type: QerySet
        qs = qs.select_related('user')
        qs = qs.prefetch_related('products')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = context.get('client')
        products = client.products.all()

        c_def = super().get_default_context_data()
        c_def['title'] = 'Клиент'
        c_def['statuses'] = [{'id': val[0], 'val': val[1]} for val in ClientsStatus.CHOICES]
        c_def['products'] = products

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterViewSet(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ClientCreationForm(request.POST)

        if form.is_valid():
            form.save()
            if settings.EMAIL_ADR_REGISTRATION:
                send_letter(inn=request.POST.get("inn"), name=request.POST.get("name"), phone=request.POST.get("phone"), email=request.POST.get("email"))
            return redirect('clients:answer')

        context = {
        }
        return render(request, template_name=self.template_name, context=context)


class AnswerViewSet(TemplateView):
    template_name = 'answer.html'
