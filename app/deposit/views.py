# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, status

from app.deposit.serializers import RecordCreateSerializer, RecordItemSerializer
from app.deposit.models import Deposit


class RecordPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class RecordListView(APIView):

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
        }
        return RecordCreateSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        amount = serializer.validated_data['amount']
        Deposit.objects.create(user=user, amount=amount, status=Deposit.STATUS_PAID)
        user.balance.add_balance(amount)
        user.balance.save()

        return Response({
            'amount': amount,
            'balance': user.balance.get_balance(),
        })

    def get(self, request, *args, **kwargs):
        queryset = Deposit.objects.filter(user=request.user)
        paginator = RecordPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = RecordItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RecordItemView(APIView):

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
        }
        return RecordItemSerializer(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        instance = Deposit.objects.filter(pk=pk)
        if not instance.exists():
            return Response({})

        serializer = self.get_serializer(instance[0])
        return Response(serializer.data)
