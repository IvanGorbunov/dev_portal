import logging
import secrets
import string
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, FormView
from django.utils.translation import gettext_lazy as _

from rest_framework.reverse import reverse_lazy

from .forms import UserForm, UserCreationForm, RegisterForm
from .models import User, Client, Stuff
from .services import add_clients_fields, add_users_context_data
from utils.views import DataMixin, ContextDataMixin


LOG = logging.getLogger(__name__)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'index.html'

    def get_success_url(self):
        return reverse_lazy('clients_requests:list')


class UserListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    @add_clients_fields
    def get_queryset(self):
        return super().get_queryset()

    @add_users_context_data({'title': 'Список пользователей', 'profile_url': 'users:users-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class UserUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = User
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:list')
    form_class = UserForm

    @add_users_context_data({'title': 'Пользователь', 'submit_url': 'users:users-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ClientListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = Client
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    @add_clients_fields
    def get_queryset(self):
        return super().get_queryset()

    @add_users_context_data({'title': 'Список пользователей - клиентов', 'profile_url': 'users:client-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ClientUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Client
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:clients-list')
    form_class = UserForm

    @add_users_context_data({'title': 'Пользователь', 'submit_url': 'users:client-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class StuffListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = Stuff
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    @add_users_context_data({'title': 'Список пользователей - сотрудников', 'profile_url': 'users:stuff-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class StuffUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Stuff
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:stuffs-list')
    form_class = UserForm

    @add_users_context_data({'title': 'Пользователь', 'submit_url': 'users:stuff-profile'})
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
