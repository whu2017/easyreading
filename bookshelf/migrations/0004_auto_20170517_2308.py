# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 15:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0003_bookshelf_create_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookshelftimestamp',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237'),
        ),
    ]
