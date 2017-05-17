# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.exceptions import NotFound
from django.db.models import ObjectDoesNotExist

from book.serializers import BookListSerializer, BookQuerySerializer, BookItemSerializer, CommentSerializer
from book.models import Book, Category, Comment
from users.models import User


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BookView(generics.ListAPIView):

    permission_classes = ()
    authentication_classes = ()
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', 'author')
    pagination_class = BookPagination

    def get(self, request, *args, **kwargs):
        serializer = BookQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        category = serializer.validated_data.get('category', '')
        category_obj = None
        if category:
            category_set = Category.objects.filter(name=category)
            if not category_set.exists():
                return Response(data={
                    "message": "图书分类不存在"
                }, status=status.HTTP_400_BAD_REQUEST)
            category_obj = category_set[0]

        if category_obj is not None:
            self.queryset = self.queryset.filter(category=category_obj)
        queryset = self.filter_queryset(self.queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookItemView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, book_id, *args, **kwargs):
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        serializer = BookItemSerializer(book)
        return Response(serializer.data)


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CommentListView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, book_id, *args, **kwargs):
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        paginator = CommentPagination()
        queryset = Comment.objects.filter(book=book, parent=None)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CommentItemView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        return Response(CommentSerializer(comment).data)


class CommentChildrenView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        paginator = CommentPagination()
        queryset = Comment.objects.filter(parent=comment)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
