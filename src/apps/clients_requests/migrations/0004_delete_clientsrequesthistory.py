# Generated by Django 4.2.8 on 2024-01-02 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients_requests', '0003_alter_clientsrequest_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientsRequestHistory',
        ),
    ]