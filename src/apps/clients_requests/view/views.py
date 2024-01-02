from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db.models import F, Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework.reverse import reverse_lazy, reverse
from rest_framework.views import APIView

from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.excel import ExportClientsRequest
from apps.clients_requests.forms import ClientsRequestItemForm, ClientsRequestItemAdminForm
from apps.clients_requests.models import ClientsRequest, ClientsRequestAttachment
from apps.clients_requests.services import update_clients_request, ClientsRequestsListMixin, add_attachments
from apps.users.choices import UserRole
from utils.views import DataMixin, ContextDataMixin, MultiSerializerViewSet


class ClientsRequestsList(LoginRequiredMixin, DataMixin, ContextDataMixin, ClientsRequestsListMixin, ListView):
    queryset = ClientsRequest.objects.filter(is_delete=False)
    context_object_name = 'clients_requests'
    template_name = 'clients_requests/clients_request_list.html'

    def get_queryset(self):
        qs = super().get_clients_request_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = super().get_default_context_data()
        c_def['title'] = "Список заявок"
        c_def['statuses'] = [{'id': val[0], 'val': val[1]} for val in StatusClientsRequest.CHOICES]
        return dict(list(context.items()) + list(c_def.items()))


class ClientsRequestCreateView(LoginRequiredMixin, ContextDataMixin, CreateView):
    model = ClientsRequest
    form_class = ClientsRequestItemForm
    template_name = 'clients_requests/clients_request_item.html'
    success_url = reverse_lazy('clients_requests:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = super().get_default_context_data()
        c_def['exclude'] = ''
        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_role_client():
            kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        if self.request.user.is_role_staff_or_admin():
            self.form_class = ClientsRequestItemAdminForm
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_role_staff_or_admin():
            self.form_class = ClientsRequestItemAdminForm
        return super().post(request, *args, **kwargs)


class ClientsRequestUpdateView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    model = ClientsRequest
    form_class = ClientsRequestItemForm
    template_name = 'clients_requests/clients_request_item.html'
    success_url = reverse_lazy('clients_requests:list')
    context_object_name = 'clients_request'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('attachments')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = super().get_default_context_data()
        c_def['statuses'] = [{'id': val[0], 'val': val[1]} for val in StatusClientsRequest.CHOICES]
        c_def['attachments'] = context['clients_request'].attachments.all()
        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_role_client():
            kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        if self.request.user.is_role_staff_or_admin():
            self.form_class = ClientsRequestItemAdminForm
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_role_client() and request.POST.get('status') != StatusClientsRequest.NEW:
            return render(request, 'not_allowed.html')

        if user.is_role_staff_or_admin():
            self.form_class = ClientsRequestItemAdminForm
            form = ClientsRequestItemAdminForm(request.POST, request.FILES)
        else:
            kwargs['user'] = user
            form = ClientsRequestItemForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            super().post(request, *args, **kwargs)
            clients_request = self.get_object()
            clients_request.save()

            add_attachments(clients_request, files=request.FILES.getlist('attachments'))

        return redirect('clients_requests:list')


class ClientsRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientsRequest
    success_url = reverse_lazy('clients_requests:list')


class ExportClientsRequestsView(LoginRequiredMixin, ClientsRequestsListMixin, MultiSerializerViewSet):
    queryset = ClientsRequest.objects.filter(is_delete=False)

    def export_to_excel(self, request, *args, **kwargs):
        qs = super().get_clients_request_queryset()

        file_bytes = ExportClientsRequest().export_to_excel(qs)
        response = HttpResponse(file_bytes)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = f'attachment; filename=' \
                                          f'{escape_uri_path("List_of_clients_requests")} ' \
                                          f'.xlsx'

        return response


class ClientsRequestAddAttachmentView(LoginRequiredMixin, MultiSerializerViewSet):
    queryset = ClientsRequestAttachment.objects.all()

    def add_attachment(self, request, *args, **kwargs):
        pk = kwargs['pk']

        file = request.FILES['file']

        attachment = ClientsRequestAttachment.objects.create(
            clients_request=pk,
            name=file.name,
            file=file.read()
        )

        return reverse('clients-request-update', args=(pk,))
