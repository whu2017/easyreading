# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if len(response.data) == 1 and 'detail' in response.data:
            response.data['message'] = response.data['detail']
            response.data.pop('detail')
        else:
            response.status_code = 422  # 验证错误, 参考：http://tools.ietf.org/html/rfc4918#section-11.2
            origin_data = response.data
            response.data = {
                'message': '验证错误',
                'errors': origin_data,
            }

    return response
