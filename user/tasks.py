# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='user.send_sms')
def send_sms():
    print('test')


@shared_task(name='user.send_email')
def send_email():
    print('test')
