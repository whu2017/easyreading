# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User


class Deposit(models.Model):
    """
    用户充值单
    """
    STATUS_UNPAID = 0
    STATUS_PAID = 1
    STATUS_FAIL = 2
    STATUS = (
        (STATUS_UNPAID, '等待付款'),
        (STATUS_PAID, '付款完成'),
        (STATUS_FAIL, '付款出错'),
    )

    user = models.ForeignKey(User, verbose_name='所属用户')
    amount = models.FloatField('充值金额')
    status = models.IntegerField('当前状态', choices=STATUS)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)
    modify_timestamp = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'deposit'
        verbose_name = '用户充值单'
        verbose_name_plural = '用户充值单'

    def __unicode__(self):
        return self.user.get_full_name() + '(DEPOSIT: %f)' % self.amount
