# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 09:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloadrecord',
            name='book',
        ),
        migrations.RemoveField(
            model_name='downloadrecord',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='buyrecord',
            options={'verbose_name': '\u8d2d\u4e70\u8bb0\u5f55\u8868', 'verbose_name_plural': '\u8d2d\u4e70\u8bb0\u5f55\u8868'},
        ),
        migrations.DeleteModel(
            name='DownloadRecord',
        ),
    ]