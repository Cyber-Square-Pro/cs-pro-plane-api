# Generated by Django 4.2.3 on 2024-02-26 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_verificationcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Workspace Name')),
                ('logo', models.URLField(blank=True, null=True, verbose_name='Logo')),
                ('slug', models.SlugField(max_length=48, unique=True)),
                ('organization_size', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_workspace', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspaces',
                'db_table': 'workspaces',
            },
        ),
    ]
