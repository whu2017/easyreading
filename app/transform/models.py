# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Transform(models.Model):
    """
    电子书转换类
    """
    STATUS_PENDING = 0
    STATUS_RUNNING = 1
    STATUS_FINISHED = 2
    STATUS_FAIL = 3
    STATUS = (
        (STATUS_PENDING, '等待中'),
        (STATUS_RUNNING, '进行中'),
        (STATUS_FINISHED, '已完成'),
        (STATUS_FAIL, '转换出错'),
    )

    origin = models.FileField(upload_to='transform/%Y/%m/%d/')
    book = models.FileField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=STATUS_PENDING)
    error_message = models.TextField('出错信息')

    class Meta:
        db_table = 'transform'
        verbose_name = '电子书转换'
        verbose_name_plural = '电子书转换'
