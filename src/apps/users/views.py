import logging
import secrets
import string

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail

from django.shortcuts import render, redirect
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


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('clients_requests:list')

    def form_valid(self, form):
        user, created = User.objects.get_or_create(email=form.cleaned_data['email'])
        new_pass = None

        if created:
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            user.set_password(new_pass)
            user.save(update_fields=['password', ])
            if settings.DEBUG:
                LOG.info(f'Created new user: {user}\n password: {new_pass}\n')

        # if new_pass or user.is_active is False:
        #     token = uuid.uuid4().hex
        #     redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
        #     cache.set(redis_key, {"buyer_id": user.id}, timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
        #
        #     confirm_link = self.request.build_absolute_uri(
        #         reverse_lazy(
        #             "web:register_confirm", kwargs={"token": token}
        #         )
        #     )
        #     message = _(f"follow this link %s \n"
        #                 f"to confirm! \n" % confirm_link)
        #     if new_pass:
        #         message += f"Your new password {new_pass} \n "
        #
        #     send_mail(
        #         subject=_("Please confirm your registration!"),
        #         message=message,
        #         from_email="soaqaa@yandex.ru",
        #         recipient_list=[user.email, ]
        #     )
        return super().form_valid(form)

# class RegisterViewSet(View):
#     template_name = 'registration/register.html'
#
#     def get(self, request, *args, **kwargs):
#         context = {
#             'form': UserCreationForm(),
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = UserCreationForm(request.POST)
#
#         # if the data is validated redirect to the main page
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('clients_requests:main_page')
#
#         # otherwise return data
#         context = {
#             'form': form
#         }
#         return render(request, self.template_name, context)


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
