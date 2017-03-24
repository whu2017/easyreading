# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import shortuuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, phone, password, is_superuser=False, **extra_fields):
        extra_fields.pop('identifier')
        now = timezone.now()
        if not email and not phone:
            raise ValueError('The given email or phone must be set')
        identifier = shortuuid.uuid()
        if email:
            email = self.normalize_email(email)
        user = self.model(identifier=identifier, email=email, phone=phone, is_superuser=is_superuser, is_staff=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password, **extra_fields):
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        return self._create_user(email, phone, password, True, **extra_fields)


class User(AbstractBaseUser):
    identifier = models.CharField('用户标识', max_length=64, unique=True)
    email = models.EmailField('Email', max_length=255, blank=True, db_index=True)
    phone = models.CharField('手机号', max_length=20, blank=True, db_index=True)
    is_superuser = models.BooleanField('超级管理员', default=False)
    is_staff = models.BooleanField('是否管理员', default=False)
    date_joined = models.DateTimeField('注册日期', default=timezone.now)

    nickname = models.CharField('昵称', max_length=64, blank=True)
    signature = models.TextField('个性签名', blank=True)

    option_sync_progress = models.BooleanField('同步进度', default=False)
    option_clean_cache = models.BooleanField('自动清除缓存', default=False)
    option_display_progress = models.BooleanField('显示阅读进度', default=True)
    option_wifi_download_only = models.BooleanField('仅用 WiFi 下载', default=True)
    option_accept_push = models.BooleanField('接受推送', default=True)
    option_auto_buy_chapter = models.BooleanField('自动购买章节', default=False)

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email', 'phone']

    def get_full_name(self):
        return self.identifier

    def get_short_name(self):
        return self.identifier

    def __unicode__(self):
        if self.email and self.phone:
            return 'ID:%d(%s,%s)' % (self.pk, self.email, self.phone)
        elif self.email:
            return 'ID:%d(%s)' % (self.pk, self.email)
        elif self.phone:
            return 'ID:%d(%s)' % (self.pk, self.phone)
        else:
            return 'ID:%d' % self.pk

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
