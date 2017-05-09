# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User


class Check(models.Model):
    """
    签到表
    """
    user = models.ForeignKey(User, verbose_name='用户')
    check_timestamp = models.DateField('签到时间', auto_now_add=True, db_index=True)

    def __unicode__(self):
        return '%s(%s)' % (self.user, self.check_timestamp)

    class Meta:
        db_table = 'check'
        verbose_name = '签到表'
        verbose_name_plural = '签到表'
