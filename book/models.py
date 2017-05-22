# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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
    author = models.CharField('作者', max_length=30, blank=True)
    cover = models.ImageField('图片', upload_to='cover/%Y/%m/%d/', blank=True)
    introduction = models.TextField('简介', blank=True)
    price = models.FloatField('价格（书币）')
    score = models.FloatField('评分')
    total_chapter = models.IntegerField('章节数量', default=0)
    latest_chapter_text = models.CharField('最近更新章节', max_length=64, blank=True)
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

    def save(self, *args, **kwargs):
        if self.cover:
            im = Image.open(self.cover)
            output = BytesIO()
            im = im.resize((1080, 1350))
            im.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.cover = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.cover.name.split('.')[0], 'image/jpeg',
                                              sys.getsizeof(output), None)
        super(Book, self).save(*args, **kwargs)


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


class SearchHistory(models.Model):
    """
    搜索历史表
    """
    user = models.ForeignKey(User, verbose_name='所属用户')
    key = models.CharField('搜索关键字', max_length=128, db_index=True)
    timestamp = models.DateTimeField('搜索时间', auto_now_add=True)

    def __unicode__(self):
        return self.key

    class Meta:
        db_table = 'search_history'
        verbose_name = '搜索历史'
        verbose_name_plural = '搜索历史'
