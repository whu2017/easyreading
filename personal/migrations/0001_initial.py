# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 19:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u56fe\u4e66')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'buy_record',
                'verbose_name': '\u8d2d\u4e70\u8868',
                'verbose_name_plural': '\u8d2d\u4e70\u8868',
            },
        ),
        migrations.CreateModel(
            name='DownloadRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u4e0b\u8f7d\u65f6\u95f4')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u56fe\u4e66')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'download_record',
                'verbose_name': '\u4e0b\u8f7d\u8868',
                'verbose_name_plural': '\u4e0b\u8f7d\u8868',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='\u82b1\u8d39\uff08\u4e66\u5e01\uff09')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u8ba2\u5355\u65e5\u671f')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u56fe\u4e66')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'order',
                'verbose_name': '\u8d26\u5355\u8868',
                'verbose_name_plural': '\u8d26\u5355\u8868',
            },
        ),
        migrations.CreateModel(
            name='ReadRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u56fe\u4e66')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'read_record',
                'verbose_name': '\u5df2\u8bfb\u8868',
                'verbose_name_plural': '\u5df2\u8bfb\u8868',
            },
        ),
    ]
