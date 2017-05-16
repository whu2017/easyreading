# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User
from book.models import Book


class Order(models.Model):
    """
    账单表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    price = models.FloatField('花费（书币）')
    timestamp = models.DateTimeField('订单日期', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'order'
        verbose_name = '账单表'
        verbose_name_plural = '账单表'


class BuyRecord(models.Model):
    """
    购买表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    timestamp = models.DateTimeField('购买日期', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'buy_record'
        verbose_name = '购买表'
        verbose_name_plural = '购买表'


class DownloadRecord(models.Model):
    """
    下载表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    timestamp = models.DateTimeField('下载时间', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'download_record'
        verbose_name = '下载表'
        verbose_name_plural = '下载表'


class ReadRecord(models.Model):
    """
    已读表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    timestamp = models.DateTimeField('添加时间', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'read_record'
        verbose_name = '已读表'
        verbose_name_plural = '已读表'
