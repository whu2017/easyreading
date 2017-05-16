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
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.TextField(max_length=256, verbose_name='\u7ae0\u8282\u6807\u8bc6\u7b26')),
                ('paragraph', models.IntegerField(verbose_name='\u6bb5\u843d\u4f4d\u79fb')),
                ('word', models.IntegerField(verbose_name='\u5b57\u4f4d\u79fb')),
                ('detail', models.TextField(verbose_name='\u4e66\u7b7e\u5185\u5bb9')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u4e66\u7b7e\u52a0\u5165\u65f6\u95f4')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u4e66\u7c4d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'bookmark',
                'verbose_name': '\u4e66\u7b7e\u8868',
                'verbose_name_plural': '\u4e66\u7b7e\u8868',
            },
        ),
        migrations.CreateModel(
            name='ReadingProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.TextField(max_length=256, verbose_name='\u7ae0\u8282\u6807\u8bc6\u7b26')),
                ('paragraph', models.IntegerField(verbose_name='\u6bb5\u843d\u4f4d\u79fb')),
                ('word', models.IntegerField(verbose_name='\u5b57\u4f4d\u79fb')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='\u4e0a\u62a5\u65f6\u95f4')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u4e66\u7c4d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'reading_progress',
                'verbose_name': '\u9605\u8bfb\u8fdb\u5ea6\u8868',
                'verbose_name_plural': '\u9605\u8bfb\u8fdb\u5ea6\u8868',
            },
        ),
    ]