# Generated by Django 4.1.7 on 2023-08-10 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Deleted')),
                ('is_secret', models.BooleanField(default=False, verbose_name='Trade secret')),
                ('content_html', models.TextField(verbose_name='Description')),
                ('type', models.CharField(choices=[('article', 'Article'), ('project', 'Project')], default='article', max_length=30, verbose_name='Type')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('on_approval', 'On approval'), ('rejected', 'Rejected'), ('agreed', 'Agreed'), ('published', 'Published'), ('on_actualization', 'On actualisation')], default='draft', max_length=30, verbose_name='Status')),
                ('access_type', models.CharField(blank=True, choices=[('all', 'All'), ('developers', 'Developers'), ('administrators', 'Administrators')], max_length=30, null=True, verbose_name='Access type')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='ArticleScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('points', 'Points'), ('duration', 'Duration')], default='points', max_length=30, verbose_name='Type')),
                ('value_points', models.IntegerField(null=True, verbose_name='Points')),
                ('value_duration', models.DurationField(null=True, verbose_name='Duration')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='article.article', verbose_name='Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_scores', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Article points',
                'verbose_name_plural': 'Articles points',
            },
        ),
        migrations.CreateModel(
            name='ArticleDurationScore',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('article.articlescore',),
        ),
        migrations.CreateModel(
            name='ArticlePointScore',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('article.articlescore',),
        ),
        migrations.CreateModel(
            name='ArticleView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='article.article', verbose_name='Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_views', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Article view',
                'verbose_name_plural': 'Articles views',
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.AddConstraint(
            model_name='articlescore',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('type', 'points'), ('value_duration__isnull', True), ('value_points__isnull', False)), models.Q(('type', 'duration'), ('value_duration__isnull', False), ('value_points__isnull', True)), _connector='OR'), name='article_articlescore_valuematches_type'),
        ),
    ]