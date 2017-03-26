# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from rest_framework_jwt.settings import api_settings


def jwt_response_payload_handler(token, user=None, request=None):
    expiration = (datetime.now() + api_settings.JWT_EXPIRATION_DELTA)
    return {
        'user_id': user.pk,
        'email': user.email,
        'phone': user.phone,
        'token': token,
        'expires_at': expiration.strftime('%s'),
    }
