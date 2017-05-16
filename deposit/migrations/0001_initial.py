# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 19:03
from __future__ import unicode_literals

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
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='\u5145\u503c\u91d1\u989d')),
                ('status', models.IntegerField(choices=[(0, '\u7b49\u5f85\u4ed8\u6b3e'), (1, '\u4ed8\u6b3e\u5b8c\u6210'), (2, '\u4ed8\u6b3e\u51fa\u9519')], verbose_name='\u5f53\u524d\u72b6\u6001')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_timestamp', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'deposit',
                'verbose_name': '\u7528\u6237\u5145\u503c\u5355',
                'verbose_name_plural': '\u7528\u6237\u5145\u503c\u5355',
            },
        ),
    ]
