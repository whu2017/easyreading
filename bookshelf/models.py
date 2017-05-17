# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User
from book.models import Book


class Bookshelf(models.Model):
    """
    书架表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    book = models.ForeignKey(Book, verbose_name='所属图书')
    create_timestamp = models.DateTimeField('加入时间', auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'bookshelf'
        verbose_name = '书架表'
        verbose_name_plural = '书架表'


class BookshelfTimestamp(models.Model):
    """
    书架更新时间记录表
    """
    user = models.OneToOneField(User, verbose_name='所属用户')
    update_timestamp = models.DateTimeField('更新时间', auto_now=True)

    def __unicode__(self):
        return '%s' % self.update_timestamp

    class Meta:
        db_table = 'bookshelf_timestamp'
        verbose_name = '书架更新时间表'
        verbose_name_plural = '书架更新时间表'
