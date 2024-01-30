from django.db.models import F


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
