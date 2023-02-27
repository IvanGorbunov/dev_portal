from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer

from apps.clients.models import Client


class MultiSerializerViewSet(ModelViewSet):
    filtersets = {
        'default': None,
    }
    serializers = {
        'default': Serializer,
    }

    @property
    def filterset_class(self):
        return self.filtersets.get(self.action) or self.filtersets.get('default')

    @property
    def serializer_class(self):
        return self.serializers.get(self.action) or self.serializers.get('default', Serializer)

    def get_response(self, data=None):
        return Response(data)

    def get_valid_data(self, many=False):
        serializer = self.get_serializer(data=self.request.data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class DataMixin:
    paginate_by = 17


class ContextDataMixin(ContextMixin):

    def get_default_context_data(self, *args, **kwargs):
        client_pk = None
        if self.request.user.is_role_client():
            client_pk = Client.objects.filter(user=self.request.user).values('id')
            if client_pk:
                client_pk = client_pk[0]['id']
        if not client_pk:
            client_pk = 0
        c_def = {
            'client_pk': str(client_pk),
            'user_is_admin': self.request.user.is_role_staff_or_admin()
        }
        return c_def
