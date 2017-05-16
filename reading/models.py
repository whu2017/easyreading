# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from users.models import User
from bookshopping.models import Book


class ReadingProgress(models.Model):
    """
    阅读进度表
    """
    book = models.ForeignKey(Book, verbose_name='所属书籍')
    user = models.ForeignKey(User, verbose_name='所属用户')
    chapter = models.TextField('章节标识符', max_length=256)
    paragraph = models.IntegerField('段落位移')
    word = models.IntegerField('字位移')
    timestamp = models.DateTimeField('上报时间', auto_now=True)

    def __unicode__(self):
        return '%s,%s,%d,%d' % (self.book, self.chapter, self.paragraph, self.word)

    class Meta:
        db_table = 'reading_progress'
        verbose_name = '阅读进度表'
        verbose_name_plural = '阅读进度表'


class Bookmark(models.Model):
    """
    书签表
    """
    book = models.ForeignKey(Book, verbose_name='所属书籍')
    user = models.ForeignKey(User, verbose_name='所属用户')
    chapter = models.TextField('章节标识符', max_length=256)
    paragraph = models.IntegerField('段落位移')
    word = models.IntegerField('字位移')
    detail = models.TextField('书签内容')
    timestamp = models.DateTimeField('书签加入时间', auto_now_add=True)

    def __unicode__(self):
        return '%s,%s,%d,%d' % (self.book, self.chapter, self.paragraph, self.word)

    class Meta:
        db_table = 'bookmark'
        verbose_name = '书签表'
        verbose_name_plural = '书签表'
