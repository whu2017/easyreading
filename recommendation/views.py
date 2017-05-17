# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import xmlrpclib

from django.conf import settings
from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from book.models import Book
from recommendation.serializers import RecommendationQuerySerializer, RecommendationBookSerializer


class IndividuationView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = RecommendationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        proxy = xmlrpclib.ServerProxy(settings.RECOMMENDATION_URL)
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
        return Response(RecommendationBookSerializer(book_set, many=True).data)


class RankView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        serializer = RecommendationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        proxy = xmlrpclib.ServerProxy(settings.RECOMMENDATION_URL)
        try:
            result = proxy.popular_recommend(amount)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        book_set = []
        for book_id in result:
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist as e:
                continue
            book_set.append(book)
        return Response(RecommendationBookSerializer(book_set, many=True).data)
