# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import base64

from django.contrib.auth.models import AnonymousUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.exceptions import NotFound
from django.db.models import ObjectDoesNotExist
from django_redis import get_redis_connection
from django.utils import timezone

from book.serializers import (
    BookListSerializer, BookQuerySerializer, BookItemSerializer, CommentDisplaySerializer, CommentPostSerializer,
)
from book.models import Book, Category, Comment, SearchHistory
from personal.models import BuyRecord, Order


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BookView(generics.ListAPIView):

    permission_classes = ()
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', 'author')
    pagination_class = BookPagination

    def get(self, request, *args, **kwargs):
        serializer = BookQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        search_term = request.query_params.get('search')
        if search_term is not None:
            conn = get_redis_connection('default')
            search_term = search_term.strip()

            # add to redis
            if search_term:
                conn.zincrby('search_hot', base64.b64encode(search_term.encode('utf-8')), amount=1)

            # add to db
            if not isinstance(request.user, AnonymousUser) and search_term:
                histories = SearchHistory.objects.filter(user=request.user, key=search_term)
                if histories.exists():
                    item = histories[0]
                    item.timestamp = timezone.now()
                    item.save()
                else:
                    SearchHistory.objects.create(user=request.user, key=search_term)

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

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, book_id, *args, **kwargs):
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        paginator = CommentPagination()
        queryset = Comment.objects.filter(book=book, parent=None)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentDisplaySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, book_id, *args, **kwargs):
        serializer = CommentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        score = serializer.validated_data.get('score', 0.0)
        content = serializer.validated_data['content']
        parent_id = serializer.validated_data['parent_id']

        if parent_id == 0:
            comment = Comment.objects.create(user=user, book=book, score=score, content=content)
        else:
            comment = Comment.objects.create(user=user, book=book, score=score, content=content, parent_id=parent_id)

        # For test only
        comment_set = Comment.objects.filter(book=book).values('score')
        score_total = 0.0
        score_count = 0
        for item in comment_set:
            score = item.get('score')
            if score > 0:
                score_count += 1
                score_total += item.get('score')
        if score_count > 0:
            score = score_total / score_count
        else:
            score = 0.0
        book.score = score
        book.save()

        return Response(CommentDisplaySerializer(comment).data)


class CommentItemView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        return Response(CommentDisplaySerializer(comment).data)


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
        serializer = CommentDisplaySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BuyView(APIView):

    def post(self, request, book_id, *args, **kwargs):
        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        balance = user.balance.get_balance()

        if BuyRecord.objects.filter(user=user, book=book).exists():
            return Response(data={'reason': '重复购买'}, status=status.HTTP_400_BAD_REQUEST)
        if balance - book.price / 100.0 < 0.0:
            return Response(data={'reason': '余额不足'}, status=status.HTTP_400_BAD_REQUEST)

        user.balance.dec_balance(book.price / 100.0)
        user.balance.save()
        BuyRecord.objects.create(user=user, book=book, price=book.price)
        Order.objects.create(user=user, amount=-book.price, name="购买图书：%s" % book.title, note="")
        return Response({
            'cost': book.price,
            'balance_book': user.balance.get_balance() * 100,
        })


class SearchHistoryView(APIView):

    def get(self, request, *args, **kwargs):
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
        resp = []
        for item in history:
            resp.append(item.key)
        return Response({
            'results': resp,
        })


class SearchHottestView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('default')
        results = conn.zrange('search_hot', 0, 10, desc=True)
        resp = []
        for item in results:
            resp.append(base64.b64decode(item).decode('utf-8'))
        return Response({
            'results': resp,
        })
