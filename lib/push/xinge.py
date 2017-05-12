# -*- coding: utf-8 -*-

from django.conf import settings
from xinge_push import XingeApp, Message, MessageIOS, ClickAction, Style
from xinge_push.constant import MESSAGE_TYPE_ANDROID_NOTIFICATION


def push_account_android(account, content, custom_args):
    """
    推送到账号中（安卓）
    :param account: 账号 
    :param content: 推送文本内容
    :param custom_args: 额外携带参数
    :return: (code, message)
    """
    return _push_account_android(account, content, custom_args)


def push_account_ios(account, content, custom_args):
    """
    推送到账号中（iOS）
    :param account: 账号 
    :param content: 推送文本内容
    :param custom_args: 额外携带参数
    :return: (code, message)
    """
    return _push_account_ios(account, content, custom_args)


def _push_account_android(account, content, custom_args):
    app = XingeApp(settings.XINGE_ANDROID_ACCESS_ID, settings.XINGE_ANDROID_SECRET_KEY)

    message = Message()
    message.type = MESSAGE_TYPE_ANDROID_NOTIFICATION
    message.content = content
    message.expireTime = 86400
    message.style = Style(0, 1, 1, 1)
    message.custom = custom_args

    action = ClickAction()
    action.actionType = ClickAction.TYPE_ACTIVITY
    action.activity = ""
    message.action = action

    return app.PushSingleAccount(0, account, message)


def _push_account_ios(account, content, custom_args):
    app = XingeApp(settings.XINGE_IOS_ACCESS_ID, settings.XINGE_IOS_SECRET_KEY)

    message = MessageIOS()
    message.expireTime = 86400
    message.alert = content
    message.badge = 1
    message.custom = custom_args

    return app.PushSingleAccount(0, account, message, 2)
