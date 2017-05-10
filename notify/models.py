# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import User


class NotifyManager(models.Manager):
    """
    通知表 Manager
    """

    def create_announce(self, content, sender):
        """
        新建公告
        :param content: 文章内容 
        :param sender: 发送者 User
        :return: Notify object
        """
        return super(NotifyManager, self).create(content=content, notify_type=Notify.NOTIFY_TYPE_ANOUNCE, target=0,
                                                 target_type=Notify.TARGET_TYPE_NULL,
                                                 action_type=Notify.ACTION_TYPE_NULL, sender=sender)

    def create_remind(self, content, target, target_type, action_type, sender):
        """
        新建提醒
        :param content: 内容
        :param target: 目标 ID
        :param target_type: 目标类型
        :param action_type: 动作
        :param sender: 发送者 User
        :return: Notify object
        """
        return super(NotifyManager, self).create(content=content, notify_type=Notify.NOTIFY_TYPE_REMIND,
                                                 target=target, target_type=target_type, action_type=action_type,
                                                 sender=sender)

    def create_message(self, content, sender, receiver):
        """
        新建消息
        :param content: 内容 
        :param sender: 发送者 User 
        :param receiver: 接收者 User
        :return: Notify object
        """
        notify = super(NotifyManager, self).create(content=content, notify_type=Notify.NOTIFY_TYPE_MESSAGE,
                                                   target=0, target_type=Notify.TARGET_TYPE_NULL,
                                                   action_type=Notify.ACTION_TYPE_NULL, sender=sender)
        return UserNotify.objects.create(user=receiver, notify=notify)

    def pull_announce(self, user):
        """
        用户拉取公告
        :param user: User object 
        :return: Pull Counter
        """
        user_notify = UserNotify.objects.filter(notify__notify_type=Notify.NOTIFY_TYPE_ANOUNCE).order_by('-create_timestamp')[:1]
        if user_notify.exists():
            create_timestamp = user_notify[0].create_timestamp
        else:
            create_timestamp = datetime(2000, 1, 1, 0, 0, 0)
        result = super(NotifyManager, self).filter(notify_type=Notify.NOTIFY_TYPE_ANOUNCE).filter(create_timestamp__gt=create_timestamp)
        pull_count = 0
        for notify in result:
            UserNotify.objects.create(user=user, notify=notify)
            pull_count += 1
        return pull_count

    def get_announce(self, user, limit=10):
        """
        获取公告
        :param user: User object 
        :return: 
        """
        return UserNotify.objects.filter(user=user, notify__notify_type=Notify.NOTIFY_TYPE_ANOUNCE).order_by('-create_timestamp')[:limit]

    def get_remind(self, user, limit=10):
        """
        获取提醒
        :param user: User object 
        :return: 
        """
        return UserNotify.objects.filter(user=user, notify__notify_type=Notify.NOTIFY_TYPE_REMIND).order_by('-create_timestamp')[:limit]

    def get_message(self, user, limit=10):
        """
        获取消息
        :param user: User object 
        :return: 
        """
        return UserNotify.objects.filter(user=user, notify__notify_type=Notify.NOTIFY_TYPE_MESSAGE).order_by('-create_timestamp')[:limit]

    def get_all(self, user, limit=10):
        """
        获取用户的全部站内消息
        :param user: User object
        :return:  
        """
        return UserNotify.objects.filter(user=user).order_by('-create_timestamp')[:limit]


class Notify(models.Model):
    """
    通知表
    """

    NOTIFY_TYPE_ANOUNCE = 0
    NOTIFY_TYPE_REMIND = 1
    NOTIFY_TYPE_MESSAGE = 2
    NOTIFY_TYPE = (
        (NOTIFY_TYPE_ANOUNCE, '公告'),
        (NOTIFY_TYPE_REMIND, '提醒'),
        (NOTIFY_TYPE_MESSAGE, '消息'),
    )

    TARGET_TYPE_NULL = ''
    TARGET_TYPE_BOOK = 'book'
    TARGET_TYPE_VIDEO = 'video'
    TARGET_TYPE_ORDER = 'order'
    TARGET_TYPE = (
        (TARGET_TYPE_NULL, '未使用'),
        (TARGET_TYPE_BOOK, '书籍'),
        (TARGET_TYPE_VIDEO, '视频'),
        (TARGET_TYPE_ORDER, '订单'),
    )

    ACTION_TYPE_NULL = ''
    ACTION_TYPE_COMMENT = 'comment'
    ACTION_TYPE_LIKE = 'like'
    ACTION_TYPE_UNLIKE = 'unlike'
    ACTION_TYPE = (
        (ACTION_TYPE_NULL, '未使用'),
        (ACTION_TYPE_COMMENT, '评论'),
        (ACTION_TYPE_LIKE, '喜欢'),
        (ACTION_TYPE_LIKE, '不喜欢'),
    )

    content = models.TextField('通知内容')
    notify_type = models.IntegerField('通知类型', choices=NOTIFY_TYPE)
    target = models.IntegerField('目标ID', default=0, blank=True)
    target_type = models.CharField('目标类型', choices=TARGET_TYPE, max_length=64, blank=True)
    action_type = models.CharField('动作类型', choices=ACTION_TYPE, max_length=64, blank=True)
    sender = models.ForeignKey(User, verbose_name='发送用户')
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)

    objects = NotifyManager()

    class Meta:
        db_table = 'notify'
        verbose_name = '通知表'
        verbose_name_plural = '通知表'

    def __unicode__(self):
        return self.content


class UserNotify(models.Model):
    """
    用户通知表
    """

    user = models.ForeignKey(User, verbose_name='所属用户')
    notify = models.ForeignKey(Notify, verbose_name='所属消息')
    is_read = models.BooleanField('是否已读', default=False)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user_notify'
        verbose_name = '用户通知表'
        verbose_name_plural = '用户通知表'

    def __unicode__(self):
        return '%s,%s' % (self.notify, self.is_read)

    def read(self):
        self.is_read = True


class Subscription(models.Model):
    """
    订阅表
    """

    user = models.ForeignKey(User, verbose_name='所属用户')
    target = models.IntegerField('目标ID')
    target_type = models.CharField('目标类型', choices=Notify.TARGET_TYPE, max_length=64)
    action_type = models.CharField('动作类型', choices=Notify.ACTION_TYPE, max_length=64)
    create_timestamp = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'subscription'
        verbose_name = '订阅表'
        verbose_name_plural = '订阅表'
