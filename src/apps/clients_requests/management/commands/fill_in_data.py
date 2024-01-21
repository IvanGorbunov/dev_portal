import random
import string

from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework import status

from apps.clients.models import Client
from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.models import ClientsRequest
from apps.products.models import Product
from apps.users.models import User


import requests


class Command(BaseCommand):
    help = 'Generate data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in range(17, 10000):
            with transaction.atomic():
                user = User.objects.create_user(
                    email=f'user_{str(i).zfill(6)}@example.com',
                )
                product = Product.objects.create(name=f'Product {str(i).zfill(6)}')

                phone_number = f'7918{str(i).zfill(7)}'
                client = Client.objects.create(
                    user=user,
                    inn=str(i).zfill(12),
                    name=f'Client {str(i).zfill(6)}',
                    phone='+7({0}{1}{2}){3}{4}{5}-{6}{7}-{8}{9}'.format(*[i for i in phone_number if i.isdigit()][1:]),
                    email=user.email,
                )
                client.products.add(product.id)
                client.save()

                for j in range(1, random.randint(1, 20)):
                    content = ''
                    api_url = f'https://api.api-ninjas.com/v1/loremipsum?max_length=255'
                    response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
                    if response.status_code == status.HTTP_200_OK:
                        content = response.text

                    client_request = ClientsRequest.objects.create(
                        title=f'Request {str(i).zfill(6)}',
                        content=content,
                        status=StatusClientsRequest.ITEMS[random.randint(0, 4)],
                        phone=client.phone,
                        email=user.email,
                        author_id=client.id,
                        product_id=product.id,
                    )
