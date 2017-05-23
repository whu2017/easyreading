# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 11:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u96be\u5ea6\u540d')),
                ('difficulty', models.IntegerField(verbose_name='\u96be\u5ea6\u7cfb\u6570')),
            ],
            options={
                'db_table': 'difficulty',
                'verbose_name': '\u96be\u5ea6\u7cfb\u6570\u8868',
                'verbose_name_plural': '\u96be\u5ea6\u7cfb\u6570\u8868',
            },
        ),
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='\u9898\u5e93\u540d')),
                ('author', models.CharField(blank=True, max_length=30, verbose_name='\u4f5c\u8005')),
                ('cover', models.ImageField(blank=True, upload_to='cover/%Y/%m/%d/', verbose_name='\u56fe\u7247')),
                ('introduction', models.TextField(blank=True, verbose_name='\u7b80\u4ecb')),
                ('price', models.FloatField(verbose_name='\u4ef7\u683c\uff08\u4e66\u5e01\uff09')),
                ('score', models.FloatField(verbose_name='\u8bc4\u5206')),
                ('question_number', models.IntegerField(default=0, verbose_name='\u9898\u76ee\u6570\u91cf')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'db_table': 'question_bank',
                'verbose_name': '\u9898\u5e93\u8868',
                'verbose_name_plural': '\u9898\u5e93\u8868',
            },
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('score', models.FloatField(default=0, verbose_name='\u8bc4\u5206')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='questionbank.QuestionComment')),
                ('question_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionbank.QuestionBank', verbose_name='\u6240\u5c5e\u9898\u5e93')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_comment', to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
            options={
                'db_table': 'question_comment',
                'verbose_name': '\u8bc4\u8bba\u8868',
                'verbose_name_plural': '\u8bc4\u8bba\u8868',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=64, verbose_name='\u95ee\u9898\u7c7b\u578b')),
                ('grade', models.IntegerField(verbose_name='\u5206\u503c')),
                ('question', models.TextField(verbose_name='\u9898\u76ee')),
                ('answer', models.TextField(verbose_name='\u7b54\u6848')),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionbank.Difficulty', verbose_name='\u96be\u5ea6')),
                ('question_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionbank', to='questionbank.QuestionBank', verbose_name='\u6240\u5c5e\u9898\u5e93')),
            ],
            options={
                'db_table': 'selection',
                'verbose_name': '\u9898\u76ee\u8868',
                'verbose_name_plural': '\u9898\u76ee\u8868',
            },
        ),
        migrations.CreateModel(
            name='SelectionOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField(verbose_name='\u9009\u9879')),
                ('selection_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selection_options', to='questionbank.Selection', verbose_name='\u6240\u5c5e\u9898\u76ee')),
            ],
            options={
                'db_table': 'option',
                'verbose_name': '\u9009\u9879\u8868',
                'verbose_name_plural': '\u9009\u9879\u8868',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=50, verbose_name='\u79d1\u76ee\u540d')),
            ],
            options={
                'db_table': 'subjects',
                'verbose_name': '\u79d1\u76ee\u8868',
                'verbose_name_plural': '\u79d1\u76ee\u8868',
            },
        ),
        migrations.AddField(
            model_name='questionbank',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionbank.Subject', verbose_name='\u79d1\u76ee'),
        ),
    ]
