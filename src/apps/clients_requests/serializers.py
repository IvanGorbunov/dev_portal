from rest_framework import serializers

from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.models import ClientsRequest
from apps.users.serializers import AuthorMixin


class StatusDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return dict(StatusClientsRequest.CHOICES)[instance]


class ClientsRequestListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField()
    inn = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    product_name = serializers.CharField()
    status = StatusDetailSerializer()

    create_dt = serializers.SerializerMethodField()
    update_dt = serializers.SerializerMethodField()

    class Meta:
        model = ClientsRequest
        fields = (
            'id',
            'title',
            'content',
            'create_dt',
            'update_dt',
            'status',
            'author',
            'product',
            'is_delete',

            'client_name',
            'inn',
            'phone',
            'email',
            'product_name',
        )

    def get_create_dt(self, clients_request: ClientsRequest):
        return clients_request.create_dt.strftime("%d.%m.%Y %H:%M:%S")

    def get_update_dt(self, clients_request: ClientsRequest):
        return clients_request.update_dt.strftime("%d.%m.%Y %H:%M:%S")


class ClientsRequestDetailSerializer(AuthorMixin, serializers.ModelSerializer):
    class Meta:
        model = ClientsRequest
        fields = '__all__'

    def create(self, validated_data):
        return ClientsRequest.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            author=self.get_req,
        )
