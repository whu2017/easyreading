# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 19:22
from __future__ import unicode_literals

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, db_index=True, max_length=255, verbose_name='Email')),
                ('phone', models.CharField(blank=True, db_index=True, max_length=20, verbose_name='\u624b\u673a\u53f7')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='\u8d85\u7ea7\u7ba1\u7406\u5458')),
                ('is_staff', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7ba1\u7406\u5458')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6ce8\u518c\u65e5\u671f')),
                ('nickname', models.CharField(blank=True, max_length=64, verbose_name='\u6635\u79f0')),
                ('signature', models.TextField(blank=True, verbose_name='\u4e2a\u6027\u7b7e\u540d')),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/%Y/%m/%d/', verbose_name='\u5934\u50cf')),
                ('option_sync_progress', models.BooleanField(default=False, verbose_name='\u540c\u6b65\u8fdb\u5ea6')),
                ('option_clean_cache', models.BooleanField(default=False, verbose_name='\u81ea\u52a8\u6e05\u9664\u7f13\u5b58')),
                ('option_display_progress', models.BooleanField(default=True, verbose_name='\u663e\u793a\u9605\u8bfb\u8fdb\u5ea6')),
                ('option_wifi_download_only', models.BooleanField(default=True, verbose_name='\u4ec5\u7528 WiFi \u4e0b\u8f7d')),
                ('option_accept_push', models.BooleanField(default=True, verbose_name='\u63a5\u53d7\u63a8\u9001')),
                ('option_auto_buy_chapter', models.BooleanField(default=False, verbose_name='\u81ea\u52a8\u8d2d\u4e70\u7ae0\u8282')),
            ],
            options={
                'db_table': 'users',
                'verbose_name': '\u7cfb\u7edf\u7528\u6237',
                'verbose_name_plural': '\u7cfb\u7edf\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='balance', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
                ('balance', models.FloatField(default=0.0, verbose_name='\u7528\u6237\u4f59\u989d')),
            ],
            options={
                'db_table': 'users_balance',
                'verbose_name': '\u7528\u6237\u7ed3\u7b97\u8868',
                'verbose_name_plural': '\u7528\u6237\u7ed3\u7b97\u8868',
            },
        ),
    ]
