import logging
import secrets
import string
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, FormView
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from rest_framework.reverse import reverse_lazy

from .choices import ClientsStatus
from .forms import ClientCreationForm
from .models import Client
from .services import send_letter, send_token
from utils.views import DataMixin, ContextDataMixin
from ..users.models import User


LOG = logging.getLogger(__name__)


class ClientsView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    queryset = Client.objects.filter(is_delete=False)
    context_object_name = 'clients'
    template_name = 'clients/clients_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = _('Clients')
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
        c_def['title'] = _('Client')
        c_def['statuses'] = [{'id': val[0], 'val': val[1]} for val in ClientsStatus.CHOICES]
        c_def['products'] = products

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = ClientCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('clients_requests:list')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user, created = User.objects.get_or_create(email=email)
        new_pass = None

        form.save()

        if created:
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            user.set_password(new_pass)
            user.save(update_fields=['password', ])
            if settings.DEBUG:
                LOG.info(f'Created new user: {user}\n password: {new_pass}\n')

        if new_pass or user.is_active is False:
            token = uuid.uuid4().hex
            redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, {'user_id': user.id}, timeout=settings.USER_CONFIRMATION_TIMEOUT)
            confirm_link = self.request.build_absolute_uri(
                reverse_lazy(
                    'clients:register-confirm', kwargs={'token': token}
                )
            )
            send_token(new_pass, email, confirm_link)

        return super().form_valid(form)


class RegisterConfirmView(View):

    def post(self, request, token, *args, **kwargs):
        redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(redis_key) or {}

        if user_id := user_info.get('user_id'):
            user = get_object_or_404(User, id=user_id)
            user.is_active = True
            user.save(update_fields=['is_active'])
            if settings.EMAIL_ADR_REGISTRATION:
                send_letter(
                    inn=request.POST.get("inn"),
                    name=request.POST.get("name"),
                    phone=request.POST.get("phone"),
                    email=request.POST.get("email")
                )
            return redirect(to=reverse_lazy('clients:answer'))
        else:
            return redirect(to=reverse_lazy('clients:register'))


class AnswerViewSet(TemplateView):
    template_name = 'answer.html'
