# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, status

from notify.models import Notify, UserNotify
from notify.serializers import UserNotifyItemSerializer
from users.models import User


class UserNotifyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class NotifyListView(APIView):

    def get(self, request, *args, **kwargs):
        Notify.objects.pull_announce(user=request.user)
        queryset = Notify.objects.get_all(request.user, 1000)
        paginator = UserNotifyPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UserNotifyItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class NotifyItemView(APIView):

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
        }
        return UserNotifyItemSerializer(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        instance = UserNotify.objects.filter(pk=pk)
        if not instance.exists():
            return Response({})

        serializer = self.get_serializer(instance[0])
        return Response(serializer.data)
