from django.db.models import F, Max

from .forms import ClientsRequestItemAdminForm, ClientsRequestItemForm
from .models import ClientsRequest, ClientsRequestAttachment


class ClientsRequestsListMixin:

    def get_clients_request_queryset(self):
        request = self.request

        date = request.GET.get('date')
        status = request.GET.get('status')
        product = request.GET.get('product')

        qs = super().get_queryset()
        if not request.user.is_role_staff_or_admin():
            qs = qs.filter(author__user=request.user)
        qs = qs.annotate(client_name=F('author__name'))
        qs = qs.annotate(inn=F('author__inn'))
        qs = qs.annotate(clients_phone=F('author__phone'))
        qs = qs.annotate(clients_email=F('author__email'))
        qs = qs.annotate(product_name=F('product__name'))
        qs = qs.order_by('-created_at')
        if date:
            date = date.split('.')
            qs = qs.filter(created_at__day=date[0])
            qs = qs.filter(created_at__month=date[1])
            qs = qs.filter(created_at__year=date[2])
        if status:
            qs = qs.filter(status=status)
        if product:
            qs = qs.filter(product__name__icontains=product)

        return qs


def update_clients_request(self, args, kwargs, request):
    if self.request.user.is_role_staff_or_admin():
        self.form_class = ClientsRequestItemAdminForm
        form = ClientsRequestItemAdminForm(request.POST, request.FILES)
    else:
        kwargs['user'] = self.request.user
        form = ClientsRequestItemForm(request.POST, request.FILES, user=self.request.user)
    if form.is_valid():
        super().post(request, *args, **kwargs)
        clients_request = self.get_object()
        clients_request.save()

        files = request.FILES.getlist('attachments')
        if files:
            clients_request = self.get_object()

            for file in files:
                max_num = ClientsRequestAttachment.objects.aggregate(Max('order_num'))['order_num__max']
                ClientsRequestAttachment.objects.create(order_num=max_num + 1, clients_request=clients_request,
                                                        name=file.name, file=file)


def add_attachments(clients_request: ClientsRequest, files: list):
    if files:
        for file in files:
            max_num = ClientsRequestAttachment.objects.aggregate(Max('order_num'))['order_num__max']
            ClientsRequestAttachment.objects.create(order_num=max_num + 1, clients_request=clients_request,
                                                    name=file.name, file=file)
