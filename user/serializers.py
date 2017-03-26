# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from calendar import timegm
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from user.compat import get_username_field, Serializer


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class LoginSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['identifier'] = serializers.CharField()
        self.fields['password'] = serializers.CharField()

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        users = User.objects.filter(email=identifier)
        if not users.exists():
            users = User.objects.filter(phone=identifier)
            if not users.exists():
                raise serializers.ValidationError('用户不存在')
        user_id = users[0].pk

        credentials = {
            self.username_field: user_id,
            'password': password,
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                payload = jwt_payload_handler(user)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                raise serializers.ValidationError('密码不正确')
        else:
            raise serializers.ValidationError('必须正确填写用户名和密码')


# class VerificationBaseSerializer(Serializer):
#     token = serializers.CharField()
#
#     def validate(self, attrs):
#         msg = 'Please define a validate method.'
#         raise NotImplementedError(msg)
#
#     def _check_payload(self, token):
#         # Check payload valid (based off of JSONWebTokenAuthentication,
#         # may want to refactor)
#         try:
#             payload = jwt_decode_handler(token)
#         except jwt.ExpiredSignature:
#             msg = _('Signature has expired.')
#             raise serializers.ValidationError(msg)
#         except jwt.DecodeError:
#             msg = _('Error decoding signature.')
#             raise serializers.ValidationError(msg)
#
#         return payload
#
#     def _check_user(self, payload):
#         username = jwt_get_username_from_payload(payload)
#
#         if not username:
#             msg = _('Invalid payload.')
#             raise serializers.ValidationError(msg)
#
#         # Make sure user exists
#         try:
#             user = User.objects.get_by_natural_key(username)
#         except User.DoesNotExist:
#             msg = _("User doesn't exist.")
#             raise serializers.ValidationError(msg)
#
#         if not user.is_active:
#             msg = _('User account is disabled.')
#             raise serializers.ValidationError(msg)
#
#         return user
#
#
# class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
#     def validate(self, attrs):
#         token = attrs['token']
#
#         payload = self._check_payload(token=token)
#         user = self._check_user(payload=payload)
#
#         return {
#             'token': token,
#             'user': user
#         }
#
#
# class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
#     def validate(self, attrs):
#         token = attrs['token']
#
#         payload = self._check_payload(token=token)
#         user = self._check_user(payload=payload)
#         # Get and check 'orig_iat'
#         orig_iat = payload.get('orig_iat')
#
#         if orig_iat:
#             # Verify expiration
#             refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
#
#             if isinstance(refresh_limit, timedelta):
#                 refresh_limit = (refresh_limit.days * 24 * 3600 +
#                                  refresh_limit.seconds)
#
#             expiration_timestamp = orig_iat + int(refresh_limit)
#             now_timestamp = timegm(datetime.utcnow().utctimetuple())
#
#             if now_timestamp > expiration_timestamp:
#                 msg = _('Refresh has expired.')
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = _('orig_iat field is required.')
#             raise serializers.ValidationError(msg)
#
#         new_payload = jwt_payload_handler(user)
#         new_payload['orig_iat'] = orig_iat
#
#         return {
#             'token': jwt_encode_handler(new_payload),
#             'user': user
#         }
