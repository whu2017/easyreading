# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import ObjectDoesNotExist
from django.utils import timezone

from book.models import Book
from bookshelf.models import Bookshelf, BookshelfTimestamp
from bookshelf.serializers import BookshelfQuerySerializer, BookshelfPutSerializer, BookshelfPostSerializer


class PersonalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BookshelfView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Bookshelf.objects.filter(user=request.user)
        paginator = PersonalPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BookshelfQuerySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookshelfPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        book_id = serializer.validated_data['book_id']

        Bookshelf.objects.get_or_create(user=user, book_id=book_id)
        try:
            timestamp = BookshelfTimestamp.objects.get(user=user)
            timestamp.update_timestamp = timezone.now()
            timestamp.save()
        except ObjectDoesNotExist:
            timestamp = BookshelfTimestamp.objects.create(user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        serializer = BookshelfPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        book_id_list = serializer.validated_data['book_id'].split(',')

        book_set = []
        for book_id in book_id_list:
            book_id = book_id.strip()
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist as e:
                return Response(data={"message": "找不到书籍 ID: %d" % book_id}, status=status.HTTP_400_BAD_REQUEST)
            book_set.append(book)

        count = len(book_set)
        Bookshelf.objects.filter(user=user).delete()
        for book in book_set:
            Bookshelf.objects.create(user=user, book=book)
        try:
            timestamp = BookshelfTimestamp.objects.get(user=user)
            timestamp.update_timestamp = timezone.now()
            timestamp.save()
        except ObjectDoesNotExist:
            timestamp = BookshelfTimestamp.objects.create(user=user)

        return Response({
            'count': count,
            'update_timestamp': timestamp.update_timestamp,
        })


class BookshelfStatusView(APIView):

    def get(self, request, *args, **kwargs):
        count = Bookshelf.objects.filter(user=request.user).count()
        bookshelf_timestamp, created = BookshelfTimestamp.objects.get_or_create(user=request.user)

        return Response({
            'count': count,
            'update_timestamp': bookshelf_timestamp.update_timestamp,
        })


class BookshelfItemView(APIView):

    def delete(self, request, book_id, *args, **kwargs):
        queryset = Bookshelf.objects.filter(user=request.user, book_id=book_id)
        if not queryset.exists():
            raise NotFound()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
