# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from personal.serializers import DepositPostSerializer, DepositItemSerializer, BuyItemSerializer, OrderSerializer, ReadSerializer
from personal.models import DepositRecord, Order, BuyRecord, ReadRecord


class PersonalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BalanceView(APIView):

    def get(self, request, *args, **kwargs):
        balance_rmb = request.user.balance.get_balance()
        return Response({
            'balance_rmb': balance_rmb,
            'balance_book': round(balance_rmb * 100, 2),
        })


class BuyingView(generics.ListAPIView):

    queryset = BuyRecord.objects.all()
    serializer_class = BuyItemSerializer
    pagination_class = PersonalPagination

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class OrderView(generics.ListAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PersonalPagination

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class DepositListView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = DepositPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        amount = serializer.validated_data['amount']
        DepositRecord.objects.create(user=user, amount=amount, status=DepositRecord.STATUS_PAID)
        user.balance.add_balance(amount)
        user.balance.save()
        Order.objects.create(user=user, amount=amount*100, name="充值", note="")

        return Response({
            'amount': amount,
            'balance_rmb': user.balance.get_balance(),
            'balance_book': user.balance.get_balance() * 100,
        })

    def get(self, request, *args, **kwargs):
        queryset = DepositRecord.objects.filter(user=request.user)
        paginator = PersonalPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = DepositItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class DepositItemView(APIView):

    def get(self, request, pk, *args, **kwargs):
        instance = DepositRecord.objects.filter(pk=pk)
        if not instance.exists():
            raise NotFound()

        serializer = DepositItemSerializer(instance[0])
        return Response(serializer.data)


class ReadView(generics.ListAPIView):

    queryset = ReadRecord.objects.all()
    serializer_class = ReadSerializer
    pagination_class = PersonalPagination

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
