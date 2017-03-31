# -*- coding: utf-8 -*-
import json
import logging

from django.conf import settings
from alidayu import api, appinfo
from alidayu.api.base import TopException
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='users.send_sms')
def send_sms(target, code):
    request = api.AlibabaAliqinFcSmsNumSendRequest()
    request.set_app_info(appinfo(settings.DAYU_APPKEY, settings.DAYU_SECRET))
    request.sms_type = 'normal'
    request.rec_num = target
    request.sms_template_code = settings.DAYU_TEMPLATE_REGISTER
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
def send_email(target, code):
    print('test')
