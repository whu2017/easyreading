# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import binascii
import random
import hashlib
import urllib
from datetime import datetime

from django import template
from django.utils.safestring import mark_safe
from rest_framework_jwt.settings import api_settings


class VerificationCode(object):
    def __init__(self, identifier, func):
        self.identifier = identifier
        self.func = func
        self.code = generate_random_code()


def jwt_response_payload_handler(token, user=None, request=None):
    expiration = (datetime.now() + api_settings.JWT_EXPIRATION_DELTA)
    return {
        'token': token,
        'expires_at': expiration.strftime('%s'),
    }


def generate_random_key():
    return binascii.hexlify(os.urandom(20)).decode()


def generate_random_code():
    return random.randint(100000, 999999)


def gravatar_url(email, size=120):
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email.lower()).hexdigest(),
        urllib.urlencode({'s': str(size)}),
    )
