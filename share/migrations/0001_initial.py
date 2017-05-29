# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 18:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('storage', '0002_auto_20170415_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShareFileLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.CharField(max_length=500)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.File')),
                ('shared_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SharedPermission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShareFolderLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.CharField(max_length=500)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.Folder')),
                ('shared_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.SharedPermission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
