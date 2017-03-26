# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.FileField(upload_to='transform/%Y/%m/%d/', verbose_name='\u539f\u59cb\u6587\u4ef6')),
                ('book', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='\u8f6c\u6362\u540e\u6587\u4ef6')),
                ('status', models.IntegerField(choices=[(0, '\u7b49\u5f85\u4e2d'), (1, '\u8fdb\u884c\u4e2d'), (2, '\u5df2\u5b8c\u6210'), (3, '\u8f6c\u6362\u51fa\u9519')], default=0, verbose_name='\u5f53\u524d\u72b6\u6001')),
                ('error_message', models.TextField(verbose_name='\u51fa\u9519\u4fe1\u606f')),
            ],
            options={
                'db_table': 'transform',
                'verbose_name': '\u7535\u5b50\u4e66\u8f6c\u6362',
                'verbose_name_plural': '\u7535\u5b50\u4e66\u8f6c\u6362',
            },
        ),
    ]