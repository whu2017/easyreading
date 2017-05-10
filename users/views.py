# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings

from users.serializers import (
    LoginSerializer, PermissionUpdateSerializer, PermissionVerifySerializer,
    IdentifierCheckSerializer, RegisterSerializer, PasswordResetSerializer,
    PasswordChangeSerializer, UserProfileSerializer
)
from users.utils import jwt_response_payload_handler, gravatar_url
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


class RegisterView(APIView):

    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get('identifier')
        password = serializer.validated_data.get('password')
        nickname = serializer.validated_data.get('nickname', '')
        if '@' in identifier:
            user = User.objects.create_user(identifier, '', password)
        else:
            user = User.objects.create_user('', identifier, password)
        user.nickname = nickname
        user.save()

        # 获取用户 Token 信息
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE, response.data['token'], expires=expiration, httponly=True)
        return response


class PasswordResetView(APIView):

    permission_classes = ()
    authentication_classes = ()
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get('identifier')
        new_password = serializer.validated_data.get('new_password')
        if '@' in identifier:
            users = User.objects.filter(email=identifier)
        else:
            users = User.objects.filter(phone=identifier)
        user = users[0]
        user.set_password(new_password)
        user.save()

        # 获取用户 Token 信息
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE, response.data['token'], expires=expiration, httponly=True)
        return response


class PasswordChangeView(APIView):

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
        }
        return PasswordChangeSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()

        # 获取用户 Token 信息
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE, response.data['token'], expires=expiration, httponly=True)
        return response


class UserProfileView(APIView):

    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'phone': user.phone,
            'balance': user.balance.balance,
            'nickname': user.nickname,
            'signature': user.signature,
            'avatar': user.avatar.url if user.avatar else '',
            'options_sync_progress': user.option_sync_progress,
            'options_clean_cache': user.option_clean_cache,
            'options_display_progress': user.option_display_progress,
            'options_wifi_download_only': user.option_wifi_download_only,
            'options_accept_push': user.option_accept_push,
            'options_auto_buy_chapter': user.option_auto_buy_chapter
        })

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        nickname = serializer.validated_data.get('nickname')
        signature = serializer.validated_data.get('signature')
        avatar = serializer.validated_data.get('avatar')
        options_sync_progress = serializer.validated_data.get('options_sync_progress')
        options_clean_cache = serializer.validated_data.get('options_clean_cache')
        options_display_progress = serializer.validated_data.get('options_display_progress')
        options_wifi_download_only = serializer.validated_data.get('options_wifi_download_only')
        options_accept_push = serializer.validated_data.get('options_accept_push')
        options_auto_buy_chapter = serializer.validated_data.get('options_auto_buy_chapter')

        if nickname is not None:
            user.nickname = nickname
        if signature is not None:
            user.signature = signature
        if avatar is not None:
            user.avatar = avatar
        if options_sync_progress is not None:
            user.option_sync_progress = options_sync_progress
        if options_clean_cache is not None:
            user.option_clean_cache = options_clean_cache
        if options_display_progress is not None:
            user.option_display_progress = options_display_progress
        if options_wifi_download_only is not None:
            user.option_wifi_download_only = options_wifi_download_only
        if options_accept_push is not None:
            user.option_accept_push = options_accept_push
        if options_auto_buy_chapter is not None:
            user.option_auto_buy_chapter = options_auto_buy_chapter
        user.save()

        return Response({
            'user_id': user.pk,
            'email': user.email,
            'phone': user.phone,
            'nickname': user.nickname,
            'signature': user.signature,
            'avatar': user.avatar.url if user.avatar else '',
            'options_sync_progress': user.option_sync_progress,
            'options_clean_cache': user.option_clean_cache,
            'options_display_progress': user.option_display_progress,
            'options_wifi_download_only': user.option_wifi_download_only,
            'options_accept_push': user.option_accept_push,
            'options_auto_buy_chapter': user.option_auto_buy_chapter
        })

