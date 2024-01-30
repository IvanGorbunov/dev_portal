from django.db.models import Max

from .forms import ClientsRequestItemAdminForm, ClientsRequestItemForm
from .models import ClientsRequest, ClientsRequestAttachment


def add_attachments(clients_request: ClientsRequest, files: list):
    if files:
        for file in files:
            max_num = ClientsRequestAttachment.objects.aggregate(Max('order_num'))['order_num__max']
            ClientsRequestAttachment.objects.create(order_num=max_num + 1, clients_request=clients_request,
                                                    name=file.name, attach_file=file)
