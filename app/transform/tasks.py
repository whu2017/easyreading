# -*- coding: utf-8 -*-

from __future__ import print_function
from celery import shared_task


class TransformTasks(object):
    """
    异步转换工具类
    """
    @shared_task(name='transform.pdf_text', bind=True)
    def pdf_text(self):
        pass
