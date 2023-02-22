# Generated by Django 4.1.7 on 2023-02-22 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients_requests', '0001_initial'),
        ('products', '0001_initial'),
        ('clients', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsrequesthistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients_requests_history_users', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='clientsrequestattachment',
            name='clients_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='clients_requests.clientsrequest', verbose_name='Clients`s request'),
        ),
        migrations.AddField(
            model_name='clientsrequest',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clients_requests', to='clients.client', verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='clientsrequest',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients_requests', to='products.product', verbose_name='Product'),
        ),
    ]
