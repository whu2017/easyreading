# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from users.serializers import (
    LoginSerializer, PermissionUpdateSerializer, PermissionVerifySerializer,
    IdentifierCheckSerializer,
)
from users.utils import jwt_response_payload_handler
from users.models import User


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
        user = serializer.object.get('users') or request.user
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


class IdentifierCheckView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = IdentifierCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get('identifier')
        user_id = serializer.validated_data.get('user_id')
        func = serializer.validated_data.get('func')
        if func == settings.FUNCTION_REGISTER and user_id is not None:
            return Response({
                'identifier': identifier,
                'available': False,
            })
        elif (func == settings.FUNCTION_UPDATE or func == settings.FUNCTION_RESET) and user_id is None:
            return Response({
                'identifier': identifier,
                'available': False,
            })
        return Response({
            'identifier': identifier,
            'available': True,
            'identifier_token': User.objects.add_verification_code(identifier, func),
        })
