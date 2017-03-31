# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.cache import cache
from django.utils import timezone

from users.utils import generate_random_key, VerificationCode
from users.tasks import send_email, send_sms


class UserManager(BaseUserManager):
    def _create_user(self, email, phone, password, is_superuser=False, **extra_fields):
        now = timezone.now()
        if not email and not phone:
            raise ValueError('The given email or phone must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, is_superuser=is_superuser, is_staff=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password, **extra_fields):
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        return self._create_user(email, phone, password, True, **extra_fields)

    def add_verification_code(self, identifier, func):
        """
        添加一个用户验证码
        :param identifier: 用户标识符
        :param func: 功能
        :return: 验证 Token
        """
        key = generate_random_key()
        value = VerificationCode(identifier, func)
        cache.set(key, value, settings.VERIFICATION_TIMEOUT)
        if '@' in identifier:
            send_email.apply_async(args=[func, identifier, str(value.code)], kwargs={})
        else:
            send_sms.apply_async(args=[func, identifier, str(value.code)], kwargs={})
        return key

    def check_verification_code(self, token, func, code):
        """
        检查一个用户验证码是否有效
        :param token: 用户 Token
        :param func: 功能
        :param code: 验证 Code
        :return: None or identifier
        """
        res = cache.get(token)
        if res is None:
            return None
        if not(hasattr(res, 'identifier') and hasattr(res, 'func') and hasattr(res, 'code')):
            return None
        if res.func != func or res.code != code:
            return None
        return res.identifier


class User(AbstractBaseUser):
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
        db_table = 'users'
        verbose_name = '系统用户'
        verbose_name_plural = '系统用户'

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'phone']

    def get_full_name(self):
        if self.email:
            return self.email
        if self.phone:
            return self.phone
        return '%s' % self.pk

    def get_short_name(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
