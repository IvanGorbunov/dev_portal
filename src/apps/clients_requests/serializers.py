from rest_framework import serializers

from .choices import StatusClientsRequest
from .models import ClientsRequest
from ..users.serializers import AuthorMixin


class StatusDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return dict(StatusClientsRequest.CHOICES)[instance]


class ClientsRequestListSerializer(serializers.ModelSerializer):
    # client_name = serializers.CharField()
    # inn = serializers.CharField()
    # phone = serializers.CharField()
    # email = serializers.EmailField()
    # # product_name = serializers.CharField()
    # status = StatusDetailSerializer()
    #
    # create_dt = serializers.SerializerMethodField()
    # update_dt = serializers.SerializerMethodField()

    class Meta:
        model = ClientsRequest
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'status',
            'author',
            'product',
            'is_delete',

            # 'client_name',
            # 'inn',
            'phone',
            'email',
            # 'product_name',
        )

    def get_create_dt(self, clients_request: ClientsRequest):
        return clients_request.created_at.strftime("%d.%m.%Y %H:%M:%S")

    def get_update_dt(self, clients_request: ClientsRequest):
        return clients_request.updated_at.strftime("%d.%m.%Y %H:%M:%S")


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
