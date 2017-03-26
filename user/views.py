# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from user.serializers import LoginSerializer, PermissionUpdateSerializer, PermissionVerifySerializer
from user.utils import jwt_response_payload_handler


class UserBaseAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE, response.data['token'], expires=expiration, httponly=True)
        return response


class LoginView(UserBaseAPIView):
    serializer_class = LoginSerializer


class PermissionVerifyView(UserBaseAPIView):
    serializer_class = PermissionVerifySerializer


class PermissionUpdateView(UserBaseAPIView):
    serializer_class = PermissionUpdateSerializer
