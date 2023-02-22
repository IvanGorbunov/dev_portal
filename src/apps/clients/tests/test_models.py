from django.test import TestCase
from rest_framework.utils import json

from apps.clients.choices import ClientsStatus
from apps.clients.models import Client, ClientsHistory
from apps.clients.tests.factories import ClientFactory
from apps.products.serializers import ProductListSerializer
from apps.users.choices import UserRole
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class TestModels(CustomViewTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(
                username='IvanovII',
                fio='Иванов Иван Иванович',
                role=UserRole.CLIENT,
                is_staff=False,
            )
        cls.client = ClientFactory(
            user=cls.user,
            inn='1234567890',
            name='ИП Иванов Иван Иванович'
        )

    def test_client_status(self):
        user = UserFactory(
            username='PetrovPP',
            fio='Петров Петр Петрович',
            role=UserRole.CLIENT,
            is_staff=False,
        )

        client = ClientFactory(
            user=user,
            inn='1234567899',
            name='ИП Петров Петр Петрович'
        )

        serializer = ProductListSerializer(client.products, many=True)
        new_values = {
            'user_id': client.user_id,
            'inn': client.inn,
            'name': client.name,
            'phone': client.phone,
            'email': client.email,
            'status': client.status,
            'is_delete': client.is_delete,
            'products': serializer.data,
        }
        values = json.dumps(new_values)

        # проверим статус в истории по умолчанию
        history = ClientsHistory.objects.filter(client=client).order_by('-date').first()
        self.assertEquals(history.values, values)

        # проверим установку нового статуса в истории
        self.client.status = ClientsStatus.ACTIV
        self.client.save()

        new_values = {
            'user_id': client.user_id,
            'inn': client.inn,
            'name': client.name,
            'phone': client.phone,
            'email': client.email,
            'status': client.status,
            'is_delete': client.is_delete,
            'products': serializer.data,
        }
        values = json.dumps(new_values)

        history = ClientsHistory.objects.filter(client=client).order_by('-date').first()
        self.assertEquals(history.values, values)

    def test_client_delete(self):
        self.client.destroy()
        request = Client.objects.filter(pk=self.client.id).first()
        self.assertEquals(request.is_delete, True)
