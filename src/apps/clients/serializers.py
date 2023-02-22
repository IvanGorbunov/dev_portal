from rest_framework import serializers

from apps.clients.models import Client
from apps.products.serializers import ProductDetailSerializer


class ClientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class ClientDetailSerializer(serializers.ModelSerializer):
    products = ProductDetailSerializer(many=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'user',
            'inn',
            'name',
            'phone',
            'email',
            'status',
            'is_delete',
            'products',
        )
