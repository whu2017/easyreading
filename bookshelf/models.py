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
    is_bought = models.BooleanField('是否已经购买', default=False)

    def __unicode__(self):
        return '%s' % self.book

    class Meta:
        db_table = 'bookshelf'
        verbose_name = '书架表'
        verbose_name_plural = '书架表'
