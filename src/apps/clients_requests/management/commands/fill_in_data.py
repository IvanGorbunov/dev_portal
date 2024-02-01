import logging
import random
from datetime import timedelta

import requests

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from rest_framework import status

from apps.article.choices import ArticleStatus, AccessType, ArticleType, ScoreType
from apps.article.models import Article, ArticleView, ArticleScore
from apps.clients.models import Client
from apps.clients_requests.choices import StatusClientsRequest
from apps.clients_requests.models import ClientsRequest
from apps.products.models import Product, Category
from apps.users.models import User


LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        LOG.info(f'Data filling started.')
        try:
            if not Product.objects.exists():

                root_1 = Category.objects.create(name=f'Root category 1')
                root_2 = Category.objects.create(name=f'Root category 2')
                root_3 = Category.objects.create(name=f'Root category 3')
                root_4 = Category.objects.create(name=f'Root category 4')

                node_1_1 = Category.objects.create(name=f'Category 1.1', parent=root_1)
                node_1_2 = Category.objects.create(name=f'Category 1.2', parent=root_1)
                node_1_3 = Category.objects.create(name=f'Category 1.3', parent=root_1)

                node_2_1 = Category.objects.create(name=f'Category 2.1', parent=root_2)
                node_2_2 = Category.objects.create(name=f'Category 2.2', parent=root_2)

                node_4_1 = Category.objects.create(name=f'Category 4.1', parent=root_4)
                node_4_2 = Category.objects.create(name=f'Category 4.2', parent=root_4)
                node_4_3 = Category.objects.create(name=f'Category 4.3', parent=root_4)

                node_4_2_1 = Category.objects.create(name=f'Category 4.2.1', parent=node_4_2)
                node_4_2_2 = Category.objects.create(name=f'Category 4.2.2', parent=node_4_2)
                node_4_2_3 = Category.objects.create(name=f'Category 4.2.3', parent=node_4_2)

                categories_list = [
                    node_1_1.id,
                    node_1_2.id,
                    node_1_3.id,
                    node_2_1.id,
                    node_2_2.id,
                    node_4_1.id,
                    node_4_3.id,
                    node_4_2_1.id,
                    node_4_2_2.id,
                    node_4_2_3.id,
                ]
                LOG.info(f' - Categories generated.')

                for pk in range(1, 31):
                    Product.objects.create(
                        name=f'Product {str(pk).zfill(6)}',
                        category_id=categories_list[random.randint(0, 9)],
                    )
                LOG.info(f' - Products generated.')
                LOG.info(f'The first step executed.')

            for i in range(1, 11):
                with transaction.atomic():
                    user = User.objects.create_user(
                        email=f'user_{str(i).zfill(6)}@example.com',
                        password=f'@User_123#{str(i).zfill(6)}',
                    )

                    product_id = random.randint(1, 30)

                    phone_number = f'7918{str(i).zfill(7)}'
                    client = Client.objects.create(
                        user=user,
                        inn=str(i).zfill(12),
                        name=f'Client {str(i).zfill(6)}',
                        phone='+7({0}{1}{2}){3}{4}{5}-{6}{7}-{8}{9}'.format(*[i for i in phone_number if i.isdigit()][1:]),
                        email=user.email,
                    )
                    client.products.add(product_id)
                    client.save()

                    for j in range(1, random.randint(1, 6)):
                        content = ''
                        api_url = f'https://baconipsum.com/api/?type=meat-and-filler'
                        response = requests.get(api_url)
                        if response.status_code == status.HTTP_200_OK:
                            content = response.text

                        ClientsRequest.objects.create(
                            title=f'Request {str(j).zfill(6)}',
                            content=content,
                            status=StatusClientsRequest.ITEMS[random.randint(0, 4)],
                            phone=client.phone,
                            email=user.email,
                            author_id=client.id,
                            product_id=product_id,
                        )
            LOG.info(f'The second step executed.')

            for product in Product.objects.all():
                with transaction.atomic():
                    for j in range(1, random.randint(1, 5)):
                        content = ''
                        api_url = f'https://baconipsum.com/api/?type=meat-and-filler'
                        response = requests.get(api_url)
                        if response.status_code == status.HTTP_200_OK:
                            content = response.text

                        article = Article.objects.create(
                            title=f'Article {str(j).zfill(6)}',
                            content_html=content,
                            is_secret=random.randint(0, 1),
                            type=ArticleType.ITEMS[random.randint(0, 1)],
                            status=ArticleStatus.ITEMS[random.randint(0, 6)],
                            access_type=AccessType.ITEMS[random.randint(0, 2)],
                            author_id=client.id,
                            product_id=product.id,
                        )

                        for _ in range(1, random.randint(1, 12)):
                            user_id = random.randint(1, User.objects.all().count())
                            if not ArticleView.objects.filter(article_id=article.id, user_id=user_id).exists():
                                ArticleView.objects.create(
                                    article_id=article.id,
                                    user_id=user_id,
                                )

                            score_type = ScoreType.ITEMS[random.randint(0, 1)]
                            duration = None
                            if score_type == ScoreType.DURATION:
                                duration = timedelta(days=-1, seconds=random.randint(10, 3600))
                            ArticleScore.objects.create(
                                article_id=article.id,
                                user_id=user_id,
                                type=score_type,
                                value_points=random.randint(10, 500) if score_type == ScoreType.POINTS else None,
                                value_duration=duration if score_type == ScoreType.DURATION else None,
                            )
                LOG.info(f' - {product.name} generated.')

            LOG.info(f'The third step executed.')
        except Exception as ex:
            LOG.error(f'Can`t generate data: {ex}')
        finally:
            LOG.info(f'Data filling ended.')
