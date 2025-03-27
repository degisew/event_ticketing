# Generated by Django 5.1.5 on 2025-03-27 11:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataLookup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('type', models.CharField(max_length=200, verbose_name='Type')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('value', models.CharField(max_length=200, unique=True, verbose_name='Value')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('category', models.CharField(blank=True, max_length=200, verbose_name='Category')),
                ('index', models.PositiveIntegerField(default=0, verbose_name='Index')),
                ('is_default', models.BooleanField(default=False, verbose_name='Is Default')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('remark', models.TextField(blank=True, verbose_name='Remark')),
            ],
            options={
                'verbose_name': 'Data Lookup',
                'verbose_name_plural': 'Data Lookups',
                'db_table': 'data_lookups',
                'constraints': [models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('type', 'is_default'), name='data_lookups_type_is_default_idx'), models.UniqueConstraint(fields=('type', 'index'), name='data_lookups_type_index_idx'), models.UniqueConstraint(fields=('value',), name='data_lookups_value_idx')],
            },
        ),
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('key', models.CharField(max_length=200, verbose_name='Key')),
                ('default_value', models.CharField(max_length=256, verbose_name='default_value')),
                ('current_value', models.CharField(max_length=256, verbose_name='current_value')),
                ('data_type', models.ForeignKey(blank=True, limit_choices_to={'type': 'data_type'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='core.datalookup')),
            ],
            options={
                'verbose_name': 'System Setting',
                'verbose_name_plural': 'System Settings',
                'db_table': 'system_settings',
                'constraints': [models.UniqueConstraint(condition=models.Q(('deleted_at__isnull', True)), fields=('key',), name='system_settings_key_idx')],
            },
        ),
    ]
