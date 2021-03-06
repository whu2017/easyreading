# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 19:28
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
            name='Bookshelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bought', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u8d2d\u4e70')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u6240\u5c5e\u56fe\u4e66')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'bookshelf',
                'verbose_name': '\u4e66\u67b6\u8868',
                'verbose_name_plural': '\u4e66\u67b6\u8868',
            },
        ),
    ]
