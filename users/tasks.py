# -*- coding: utf-8 -*-
import json
import logging

import emails
from emails.template import JinjaTemplate as T
from django.conf import settings
from alidayu import api, appinfo
from alidayu.api.base import TopException
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='users.send_sms')
def send_sms(func, target, code):
    request = api.AlibabaAliqinFcSmsNumSendRequest()
    request.set_app_info(appinfo(settings.DAYU_APPKEY, settings.DAYU_SECRET))
    request.sms_type = 'normal'
    request.rec_num = target
    if func == settings.FUNCTION_REGISTER:
        request.sms_template_code = settings.DAYU_TEMPLATE_REGISTER
    elif func == settings.FUNCTION_UPDATE:
        request.sms_template_code = settings.DAYU_TEMPLATE_UPDATE
    elif func == settings.FUNCTION_RESET:
        request.sms_template_code = settings.DAYU_TEMPLATE_RESET
    else:
        logger.warning('invalid function parameter %s' % func)
        return
    request.sms_free_sign_name = settings.DAYU_SIGNATURE
    request.sms_param = {'code': code}
    try:
        response = request.getResponse()
    except TopException as e:
        logger.warning('cannot send sms, target=%s, code=%s. %s, %s' % (target, code, e.message, e.subcode))
        return
    try:
        if not response['alibaba_aliqin_fc_sms_num_send_response']['result']['success']:
            raise ValueError
    except (IndexError, ValueError):
        logger.warning('invalid sms response, target=%s, code=%s. %s' % (target, code, json.dumps(response)))
        return
    logger.info('sms has sent, target=%s, code=%s' % (target, code))


@shared_task(name='users.send_email')
def send_email(func, target, code):
    if func == settings.FUNCTION_REGISTER:
        content = T(u"<html><p>您正在进行用户注册操作，验证码 {{ code }}，请在 15 分钟内按提示提交验证码。")
    elif func == settings.FUNCTION_UPDATE:
        content = T(u"<html><p>您正在进行手机号更新操作，验证码 {{ code }}，请在 15 分钟内按提示提交验证码。")
    elif func == settings.FUNCTION_RESET:
        content = T(u"<html><p>您正在进行密码重置操作，验证码 {{ code }}，请在 15 分钟内按提示提交验证码。")
    else:
        logger.warning('invalid function parameter %s' % func)
        return

    m = emails.Message(
        html=content,
        subject=T(u"随阅易手机阅读 - 验证码"),
        mail_from=(u"随阅易手机阅读", settings.SMTP_FROM),
    )
    response = m.send(
        render={
            "code": code,
        },
        to=target,
        smtp={
            "host": settings.SMTP_SERVER,
            "port": settings.SMTP_PORT,
            'ssl': True,
            'user': settings.SMTP_FROM,
            'password': settings.SMTP_PASSWORD,
        },
    )
    if response.status_code not in [250, ]:
        logger.warning('cannot send email, target=%s, code=%s. %s' % (target, code, str(response)))
        return
    logger.info('email has sent, target=%s, code=%s' % (target, code))
