# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from check.models import Check


class CheckView(APIView):

    def get(self, request, *args, **kwargs):
        total = Check.objects.filter(user=request.user).count()
        now = datetime.now()
        result = Check.objects.filter(
            user=request.user,
            check_timestamp__year=now.year,
            check_timestamp__month=now.month,
            check_timestamp__day=now.day,
        )
        return Response({
            'total': total,
            'is_check_today': True if result.exists() else False,
        })

    def post(self, request, *args, **kwargs):
        now = datetime.now()
        result = Check.objects.filter(
            user=request.user,
            check_timestamp__year=now.year,
            check_timestamp__month=now.month,
            check_timestamp__day=now.day,
        )
        if result.exists():
            return Response({
                'status': 'repeat check',
            })

        Check.objects.create(user=request.user)
        return Response({
            'status': 'ok',
        })
