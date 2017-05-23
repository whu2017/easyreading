# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import User


class Subject(models.Model):
    """
    科目
    """
    subject_name = models.CharField('科目名', max_length=50)

    def __unicode__(self):
        return '%s' % self.subject_name

    class Meta:
        db_table = 'subjects'
        verbose_name = '科目表'
        verbose_name_plural = '科目表'


class QuestionBank (models.Model):
    title = models.CharField('题库名', max_length=30)
    subject = models.ForeignKey(Subject, verbose_name='科目')
    author = models.CharField('作者', max_length=30, blank=True)
    cover = models.ImageField('图片', upload_to='cover/%Y/%m/%d/', blank=True)
    introduction = models.TextField('简介', blank=True)
    price = models.FloatField('价格（书币）')
    score = models.FloatField('评分')
    question_number = models.IntegerField('题目数量', default=0)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)
    update_timestamp = models.DateTimeField('更新时间', auto_now=True)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        db_table = 'question_bank'
        verbose_name = '题库表'
        verbose_name_plural = '题库表'


class QuestionComment(MPTTModel):
    """
    评论表
    """
    user = models.ForeignKey(User, verbose_name='所属用户', related_name='question_comment')
    question_bank = models.ForeignKey(QuestionBank, verbose_name='所属题库')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    content = models.TextField('评论内容')
    score = models.FloatField('评分', default=0)
    timestamp = models.DateTimeField('评论时间', auto_now_add=True)

    def __unicode__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['-timestamp']

    class Meta:
        db_table = 'question_comment'
        verbose_name = '评论表'
        verbose_name_plural = '评论表'


class Difficulty(models.Model):
    """
    难度系数
    """
    name = models.CharField('难度名', max_length=30)
    difficulty = models.IntegerField('难度系数')

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'difficulty'
        verbose_name = '难度系数表'
        verbose_name_plural = '难度系数表'


class Selection(models.Model):
    """
    选择类题
    """
    question_type = models.CharField('问题类型', max_length=64)
    question_bank = models.ForeignKey(QuestionBank, verbose_name='所属题库', related_name='questionbank')
    grade = models.IntegerField('分值')
    question = models.TextField('题目')
    difficulty = models.ForeignKey(Difficulty, verbose_name='难度')
    answer = models.TextField('答案')

    def __unicode__(self):
        return '%s' % self.question

    class Meta:
        db_table = 'selection'
        verbose_name = '题目表'
        verbose_name_plural = '题目表'


class SelectionOptions(models.Model):
    selection_name = models.ForeignKey(Selection, verbose_name='所属题目', related_name='selection_options')
    option = models.TextField('选项')

    def __unicode__(self):
        return '%s' % self.selection_name

    class Meta:
        db_table = 'option'
        verbose_name = '选项表'
        verbose_name_plural = '选项表'
