# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


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


class FillBlanks(models.Model):
    """
    填空题
    """
    question_type = "fill_blanks"
    subject = models.ForeignKey(Subject, verbose_name='科目')
    score = models.IntegerField('分值')
    question = models.TextField('题目')
    answer = models.CharField('答案', max_length=50)
    difficulty = models.ForeignKey(Difficulty, verbose_name='难度')

    def __unicode__(self):
        return '%s' % self.question

    class Meta:
        db_table = 'fill_blanks'
        verbose_name = '填空题表'
        verbose_name_plural = '填空题表'


class MultiSelection(models.Model):
    """
    多选题
    """
    question_type = "multi_selection"
    subject = models.ForeignKey(Subject, verbose_name='科目')
    score = models.IntegerField('分值')
    question = models.TextField('题目')
    selectionA = models.TextField('选项A')
    selectionB = models.TextField('选项B')
    selectionC = models.TextField('选项C')
    selectionD = models.TextField('选项D')
    selectionE = models.TextField('选项E')
    selectionF = models.TextField('选项F')
    answer = models.CharField('答案', max_length=6)
    difficulty = models.ForeignKey(Difficulty, verbose_name='难度')

    def __unicode__(self):
        return '%s' % self.question

    class Meta:
        db_table = 'multi_selection'
        verbose_name = '多选题表'
        verbose_name_plural = '多选题表'


class SingleSelection(models.Model):
    """
    选择题
    """
    question_type = "single_selection"
    subject = models.ForeignKey(Subject, verbose_name='科目')
    score = models.IntegerField('分值')
    question = models.TextField('题目')
    selectionA = models.TextField('选项A')
    selectionB = models.TextField('选项B')
    selectionC = models.TextField('选项C')
    selectionD = models.TextField('选项D')
    answer = models.CharField(max_length=1)
    difficulty = models.ForeignKey(Difficulty, verbose_name='难度')

    def __unicode__(self):
        return '%s' % self.question

    class Meta:
        db_table = 'single_selection'
        verbose_name = '单选题表'
        verbose_name_plural = '单选题表'


class Judge(models.Model):
    """
    判断题
    """
    question_type = "judgement"
    subject = models.ForeignKey(Subject, verbose_name='科目')
    score = models.IntegerField('分值')
    question = models.TextField('题目')
    answer = models.BooleanField('正确')
    difficulty = models.ForeignKey(Difficulty, verbose_name='难度')

    def __unicode__(self):
        return '%s' % self.question

    class Meta:
        db_table = 'judge'
        verbose_name = '判断题表'
        verbose_name_plural = '判断题表'
