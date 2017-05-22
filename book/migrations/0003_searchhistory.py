# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 14:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0002_auto_20170517_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128, verbose_name='\u641c\u7d22\u5173\u952e\u5b57')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u641c\u7d22\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'search_history',
                'verbose_name': '\u641c\u7d22\u5386\u53f2',
                'verbose_name_plural': '\u641c\u7d22\u5386\u53f2',
            },
        ),
    ]