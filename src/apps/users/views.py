from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from rest_framework.reverse import reverse_lazy

from apps.users.forms import UserForm, UserCreationForm
from apps.users.models import User, Client, Stuff
from utils.views import DataMixin, ContextDataMixin


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'index.html'

    def get_success_url(self):
        return reverse_lazy('clients_requests:list')


class RegisterViewSet(View):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        # if the data is validated redirect to the main page
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('clients_requests:main_page')

        # otherwise return data
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class UserListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(agent_id=F('agent__id'))
        qs = qs.annotate(agent_name=F('agent__name'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список пользователей'
        c_def['profile_url'] = 'users:users-profile'

        return dict(list(context.items()) + list(c_def.items()))


class UserUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = User
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:list')
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Пользователь'
        c_def['submit_url'] = 'users:users-profile'

        return dict(list(context.items()) + list(c_def.items()))


class ClientListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = Client
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(agent_id=F('agent__id'))
        qs = qs.annotate(agent_name=F('agent__name'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список пользователей - клиентов'
        c_def['profile_url'] = 'users:client-profile'

        return dict(list(context.items()) + list(c_def.items()))


class ClientUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Client
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:clients-list')
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Пользователь'
        c_def['submit_url'] = 'users:client-profile'

        return dict(list(context.items()) + list(c_def.items()))


class StuffListView(LoginRequiredMixin, ContextDataMixin, DataMixin, ListView):
    model = Stuff
    context_object_name = 'users'
    template_name = 'users/users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Список пользователей - сотрудников'
        c_def['profile_url'] = 'users:stuff-profile'

        return dict(list(context.items()) + list(c_def.items()))


class StuffUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = Stuff
    template_name = 'users/users_profile.html'
    success_url = reverse_lazy('users:stuffs-list')
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = 'Пользователь'
        c_def['submit_url'] = 'users:stuff-profile'

        return dict(list(context.items()) + list(c_def.items()))
