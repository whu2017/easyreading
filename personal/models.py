# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User
from book.models import Book


class BuyRecord(models.Model):
    """
    购买记录表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    price = models.FloatField('花费（书币）', default=0.0)
    timestamp = models.DateTimeField('购买日期', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'buy_record'
        verbose_name = '购买记录表'
        verbose_name_plural = '购买记录表'


class DepositRecord(models.Model):
    """
    充值记录表
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
    amount = models.FloatField('金额（书币）')
    status = models.IntegerField('当前状态', choices=STATUS)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)
    modify_timestamp = models.DateTimeField('最后修改时间', auto_now=True)

    def __unicode__(self):
        return self.user.get_full_name() + '(DEPOSIT: %f)' % self.amount

    class Meta:
        db_table = 'deposit_record'
        verbose_name = '充值记录表'
        verbose_name_plural = '充值记录表'


class Order(models.Model):
    """
    账单表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    amount = models.FloatField('金额变动（书币）')
    name = models.CharField('商品名称', max_length=256)
    note = models.TextField('订单备注', blank=True)
    timestamp = models.DateTimeField('订单日期', auto_now_add=True)

    def __unicode__(self):
        return '%s. %s' % (self.name, self.note)

    class Meta:
        db_table = 'order'
        verbose_name = '账单表'
        verbose_name_plural = '账单表'


class ReadRecord(models.Model):
    """
    已读书籍表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    timestamp = models.DateTimeField('添加时间', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'read_record'
        verbose_name = '已读书籍表'
        verbose_name_plural = '已读书籍表'
