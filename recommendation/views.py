# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import xmlrpclib

from django.conf import settings
from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from book.models import Book
from recommendation.serializers import RecommendationQuerySerializer, RecommendationBookSerializer


class RecommendationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class IndividuationView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = RecommendationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        proxy = xmlrpclib.ServerProxy(settings.RECOMMENDATION_URL, allow_none=True)
        try:
            result = proxy.personalized_recommend(request.user.pk, amount)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        book_set = []
        for book_id in result:
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist as e:
                continue
            book_set.append(book)

        paginator = RecommendationPagination()
        result_page = paginator.paginate_queryset(book_set, request)
        serializer = RecommendationBookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RankView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        serializer = RecommendationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        proxy = xmlrpclib.ServerProxy(settings.RECOMMENDATION_URL, allow_none=True)
        try:
            result = proxy.popular_recommend(None, amount)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        book_set = []
        for book_id in result:
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist as e:
                continue
            book_set.append(book)

        paginator = RecommendationPagination()
        result_page = paginator.paginate_queryset(book_set, request)
        serializer = RecommendationBookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
