# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 09:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20161219_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Karma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='karma',
        ),
        migrations.AddField(
            model_name='karma',
            name='giver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='giver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='karma',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
