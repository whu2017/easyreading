# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 07:14
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
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u901a\u77e5\u5185\u5bb9')),
                ('notify_type', models.IntegerField(choices=[(0, '\u516c\u544a'), (1, '\u63d0\u9192'), (2, '\u6d88\u606f')], verbose_name='\u901a\u77e5\u7c7b\u578b')),
                ('target', models.IntegerField(verbose_name='\u76ee\u6807ID')),
                ('target_type', models.CharField(choices=[('', '\u672a\u4f7f\u7528'), ('book', '\u4e66\u7c4d'), ('video', '\u89c6\u9891'), ('order', '\u8ba2\u5355')], max_length=64, verbose_name='\u76ee\u6807\u7c7b\u578b')),
                ('action_type', models.CharField(choices=[('', '\u672a\u4f7f\u7528'), ('comment', '\u8bc4\u8bba'), ('like', '\u559c\u6b22'), ('like', '\u4e0d\u559c\u6b22')], max_length=64, verbose_name='\u52a8\u4f5c\u7c7b\u578b')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u9001\u7528\u6237')),
            ],
            options={
                'db_table': 'notify',
                'verbose_name': '\u901a\u77e5\u8868',
                'verbose_name_plural': '\u901a\u77e5\u8868',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.IntegerField(verbose_name='\u76ee\u6807ID')),
                ('target_type', models.CharField(choices=[('', '\u672a\u4f7f\u7528'), ('book', '\u4e66\u7c4d'), ('video', '\u89c6\u9891'), ('order', '\u8ba2\u5355')], max_length=64, verbose_name='\u76ee\u6807\u7c7b\u578b')),
                ('action_type', models.CharField(choices=[('', '\u672a\u4f7f\u7528'), ('comment', '\u8bc4\u8bba'), ('like', '\u559c\u6b22'), ('like', '\u4e0d\u559c\u6b22')], max_length=64, verbose_name='\u52a8\u4f5c\u7c7b\u578b')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'subscription',
                'verbose_name': '\u8ba2\u9605\u8868',
                'verbose_name_plural': '\u8ba2\u9605\u8868',
            },
        ),
        migrations.CreateModel(
            name='UserNotify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u8bfb')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('notify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notify.Notify', verbose_name='\u6240\u5c5e\u6d88\u606f')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'user_notify',
                'verbose_name': '\u7528\u6237\u901a\u77e5\u8868',
                'verbose_name_plural': '\u7528\u6237\u901a\u77e5\u8868',
            },
        ),
    ]