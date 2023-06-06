from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.clients_requests.models import ClientsRequest
from apps.clients_requests.serializers import ClientsRequestListSerializer


class ClientsRequestsViewSet(viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin):

    queryset = ClientsRequest.objects.all()

    serializer_class = ClientsRequestListSerializer
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter)
    # filterset_class = TransactionFilter
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    search_fields = [
        'title',
        'create_dt',
        'status',
        'phone',
        'email',
        'author',
        'product',
    ]
    order_by = ['id', ]



    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
