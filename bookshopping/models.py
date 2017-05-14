# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User

from mptt.models import MPTTModel, TreeForeignKey


class BookClass(models.Model):
    """
    图书类表
    """
    book_class_name = models.CharField('图书类名', max_length=30)

    def __unicode__(self):
        return '%s' % self.book_class_name

    class Meta:
        db_table = 'book_class'
        verbose_name = '图书类表'
        verbose_name_plural = '图书类表'


class BookInfo(models.Model):
    """
    图书信息表
    """
    book_class = models.ForeignKey(BookClass, verbose_name='图书类表')
    title = models.CharField('书名', max_length=30)
    price = models.FloatField('价格')
    data = models.TextField('简介')
    cover = models.ImageField('图片', upload_to='cover/%Y/%m/%d/', blank=True)
    author = models.CharField('作者', max_length=30)
    score = models.FloatField('评分')
    time = models.DateTimeField('更新时间')
    chapter = models.CharField('最近更新章节', max_length=30)

    def __unicode__(self):
        return '%s' % self.book_class

    class Meta:
        db_table = 'book_info'
        verbose_name = '图书信息表'
        verbose_name_plural = '图书信息表'


class Bookcase(models.Model):
    """
    书架表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')

    def __unicode__(self):
        return '%d' % self.book_info.pk

    class Meta:
        db_table = 'bookcase'
        verbose_name = '书架表'
        verbose_name_plural = '书架表'


class Comment(MPTTModel):
    """
    评论表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')
    comment_time = models.DateTimeField('评论时间')
    comment_contain = models.TextField('评论内容')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    comment_score = models.IntegerField('评论分数')

    def __unicode__(self):
        return '%d' % self.book_info.pk

    class MPTTMeta:
        order_insertion_by = ['comment_time']


class ShoppingList(models.Model):
    """
    账单表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')
    buy_time = models.DateTimeField('购买日期')
    price = models.FloatField('花费')

    def __unicode__(self):
        return '%s' % self.book_info.pk

    class Meta:
        db_table = 'shopping_list'
        verbose_name = '账单表'
        verbose_name_plural = '账单表'


class BuyRecord(models.Model):
    """
    购买表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')
    add_time = models.DateTimeField('添加时间')

    def __unicode__(self):
        return '%s' % self.book_info.pk

    class Meta:
        db_table = 'buy_record'
        verbose_name = '购买表'
        verbose_name_plural = '购买表'


class DownloadRecord(models.Model):
    """
    下载表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')
    add_time = models.DateTimeField('添加时间')

    def __unicode__(self):
        return '%s' % self.book_info.pk

    class Meta:
        db_table = 'download_record'
        verbose_name = '下载表'
        verbose_name_plural = '下载表'


class ReadRecord(models.Model):
    """
    已读表
    """
    book_info = models.ForeignKey(BookInfo, verbose_name='图书信息表')
    user = models.ForeignKey(User, verbose_name='用户')
    add_time = models.DateTimeField('添加时间')

    def __unicode__(self):
        return '%s' % self.book_info.pk

    class Meta:
        db_table = 'read_record'
        verbose_name = '已读表'
        verbose_name_plural = '已读表'