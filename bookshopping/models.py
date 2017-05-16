# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from users.models import User
from transform.models import Transform


class Category(models.Model):
    """
    图书分类表
    """
    name = models.CharField('分类名称', max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '图书分类表'
        verbose_name_plural = '图书分类表'


class Book(models.Model):
    """
    图书表
    """
    category = models.ForeignKey(Category, verbose_name='所属分类')
    title = models.CharField('书名', max_length=30)
    author = models.CharField('作者', max_length=30)
    cover = models.ImageField('图片', upload_to='cover/%Y/%m/%d/', blank=True)
    introduction = models.TextField('简介')
    price = models.FloatField('价格（书币）')
    score = models.FloatField('评分')
    total_chapter = models.IntegerField('章节数量')
    latest_chapter_text = models.CharField('最近更新章节', max_length=64)
    allow_trial = models.BooleanField('是否允许试读', default=True)
    trial_chapter = models.PositiveIntegerField('试读允许章节', default=1)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)
    update_timestamp = models.DateTimeField('更新时间', auto_now=True)
    resource = models.ForeignKey(Transform, verbose_name='图书文件')

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'book'
        verbose_name = '图书表'
        verbose_name_plural = '图书表'


class Bookshelf(models.Model):
    """
    书架表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    is_bought = models.BooleanField('是否已经购买', default=False)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'bookcase'
        verbose_name = '书架表'
        verbose_name_plural = '书架表'


class Comment(MPTTModel):
    """
    评论表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    content = models.TextField('评论内容')
    score = models.FloatField('评分', default=0)
    timestamp = models.DateTimeField('评论时间', auto_now_add=True)

    def __unicode__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['-timestamp']

    class Meta:
        db_table = 'comment'
        verbose_name = '评论表'
        verbose_name_plural = '评论表'


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
