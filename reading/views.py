# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import mixins, status

from bookshopping.models import BookInfo
from reading.serializers import ReadingProgressSerializer
from reading.models import ReadingProgress


class ReadingProgressView(APIView):

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
        }
        return ReadingProgressSerializer(*args, **kwargs)

    def put(self, request, book_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            book = BookInfo.objects.get(pk=book_id)
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
            book = BookInfo.objects.get(pk=book_id)
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
