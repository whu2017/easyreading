# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from user.serializers import LoginSerializer
from user.utils import jwt_response_payload_handler


class BaseUserAPIView(APIView):
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
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, response.data['token'], expires=expiration, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(BaseUserAPIView):
    serializer_class = LoginSerializer


# class VerifyJSONWebToken(JSONWebTokenAPIView):
#     """
#     API View that checks the veracity of a token, returning the token if it
#     is valid.
#     """
#     serializer_class = VerifyJSONWebTokenSerializer
#
#
# class RefreshJSONWebToken(JSONWebTokenAPIView):
#     """
#     API View that returns a refreshed token (with new expiration) based on
#     existing token
#
#     If 'orig_iat' field (original issued-at-time) is found, will first check
#     if it's within expiration window, then copy it to the new token
#     """
#     serializer_class = RefreshJSONWebTokenSerializer
#
#
# obtain_jwt_token = ObtainJSONWebToken.as_view()
# refresh_jwt_token = RefreshJSONWebToken.as_view()
# verify_jwt_token = VerifyJSONWebToken.as_view()
