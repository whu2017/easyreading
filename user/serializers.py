# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from calendar import timegm
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import authenticate, get_user_model
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


class PermissionBaseSerializer(Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        raise NotImplementedError('Must define a validate method')

    def _check_payload(self, token):
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise serializers.ValidationError('Token 已过期')
        except jwt.DecodeError:
            raise serializers.ValidationError('无法解析 Token')
        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)
        if not username:
            raise serializers.ValidationError('无效的用户信息')
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户不存在')
        return user


# class VerifyJSONWebTokenSerializer(PermissionBaseSerializer):
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


class PermissionUpdateSerializer(PermissionBaseSerializer):
    def validate(self, attrs):
        token = attrs['token']
        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        new_payload = jwt_payload_handler(user)
        return {
            'token': jwt_encode_handler(new_payload),
            'user': user
        }
