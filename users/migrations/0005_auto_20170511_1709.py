# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-11 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatar/%Y/%m/%d/', verbose_name='\u5934\u50cf'),
        ),
    ]
