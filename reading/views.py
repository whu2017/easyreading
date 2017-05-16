# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import mixins, status

from bookshopping.models import Book
from reading.serializers import ReadingProgressSerializer, BookmarkSerializer, BookmarkGetSerializer
from reading.models import ReadingProgress, Bookmark


class BookmarkView(APIView):

    def get(self, request, book_id, *args, **kwargs):
        serializer = BookmarkGetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        result = Bookmark.objects.filter(user=user, book=book)
        return Response({
            "results": result.values('id', 'chapter', 'paragraph', 'word', 'detail', 'timestamp'),
        })

    def post(self, request, book_id, *args, **kwargs):
        serializer = BookmarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        chapter = serializer.validated_data['chapter']
        paragraph = serializer.validated_data['paragraph']
        word = serializer.validated_data['word']

        bookmark = Bookmark.objects.create(user=user, book=book, chapter=chapter, paragraph=paragraph, word=word, detail="")
        return Response({
            "chapter": bookmark.chapter,
            "paragraph": bookmark.paragraph,
            "word": bookmark.word,
            "detail": bookmark.detail,
            "timestamp": bookmark.timestamp,
        })


class BookmarkItemView(APIView):

    def delete(self, request, book_id, bookmark_id, *args, **kwargs):
        try:
            bookmark = Bookmark.objects.get(pk=bookmark_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        if bookmark.book.id != int(book_id):
            raise NotFound()

        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadingProgressView(APIView):

    def put(self, request, book_id, *args, **kwargs):
        serializer = ReadingProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        chapter = serializer.validated_data['chapter']
        paragraph = serializer.validated_data['paragraph']
        word = serializer.validated_data['word']

        result = ReadingProgress.objects.filter(user=user, book=book)
        if result.exists():
            progress = result[0]
            progress.chapter = chapter
            progress.paragraph = paragraph
            progress.word = word
            progress.save()
        else:
            progress = ReadingProgress.objects.create(user=user, book=book, chapter=chapter, paragraph=paragraph, word=word)

        return Response({
            "chapter": progress.chapter,
            "paragraph": progress.paragraph,
            "word": progress.word,
            "timestamp": progress.timestamp,
        })

    def get(self, request, book_id, *args, **kwargs):
        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        result = ReadingProgress.objects.filter(user=user, book=book)
        if result.exists():
            progress = result[0]
        else:
            # TODO 待修改 chapter
            progress = ReadingProgress.objects.create(user=user, book=book, chapter="", paragraph=0, word=0)

        return Response({
            "chapter": progress.chapter,
            "paragraph": progress.paragraph,
            "word": progress.word,
            "timestamp": progress.timestamp,
        })
