# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    用户详细信息 Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField('昵称', max_length=64)
    phone = models.CharField('手机号码', max_length=20)
    signature = models.TextField('个性签名')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'


class UserOptions(models.Model):
    """
    用户个人选项 Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sync_progress = models.BooleanField('是否同步进度', default=False)
    clean_cache = models.BooleanField('是否自动清除缓存', default=False)
    display_progress = models.BooleanField('是否显示阅读进度', default=True)
    wifi_download_only = models.BooleanField('是否仅用 WiFi 下载', default=True)
    accept_push = models.BooleanField('是否接受推送', default=True)
    auto_buy_chapter = models.BooleanField('是否自动购买章节', default=False)

    class Meta:
        db_table = 'user_options'
        verbose_name = '用户选项'
        verbose_name_plural = '用户选项'
