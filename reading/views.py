# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import mixins, status

from book.models import Book
from personal.models import BuyRecord, ReadRecord
from reading.serializers import ReadingProgressSerializer, BookmarkSerializer, BookmarkGetSerializer, ChapterSerializer
from reading.models import ReadingProgress, Bookmark
from lib.parser.epub import parse_structure, chapter_content


class BookView(APIView):

    def get(self, request, book_id, *args, **kwargs):
        user = request.user
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        is_bought = False
        if BuyRecord.objects.filter(user=user, book=book).exists():
            is_bought = True
        structure = parse_structure(book.resource.final.path)

        return Response({
            "info": {
                "id": book.pk,
                "category_id": book.category.pk,
                "category_name": book.category.name,
                "title": book.title,
                "author": book.author,
                "cover": book.cover.url if book.cover else '',
                "introduction": book.introduction,
                "price": book.price,
                "score": book.score,
                "total_chapter": book.total_chapter,
                "latest_chapter_text": book.latest_chapter_text,
                "allow_trial": book.allow_trial,
                "trial_chapter": book.trial_chapter,
                "create_timestamp": book.create_timestamp,
                "update_timestamp": book.update_timestamp,
                "is_bought": is_bought,
            },
            "structure": structure,
        })


class ChapterView(APIView):

    def get_serializer(self, data, book_id, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'view': self,
            'book_id': book_id,
        }
        return ChapterSerializer(data=data, *args, **kwargs)

    def get(self, request, book_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params, book_id=book_id)
        serializer.is_valid(raise_exception=True)

        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        identifier = serializer.validated_data['identifier']

        paragraphs = chapter_content(book.resource.final.path, identifier)
        return Response({
            'chapter': paragraphs[0] if len(paragraphs) > 0 else '',
            'identifier': identifier,
            'paragraphs': paragraphs[1:] if len(paragraphs) > 0 else paragraphs,
        })


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

        # 添加已读记录
        ReadRecord.objects.get_or_create(user=user, book=book)

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
            structure = parse_structure(book.resource.final.path)
            chapter = structure[0].chapter if len(structure) > 0 else ''
            progress = ReadingProgress.objects.create(user=user, book=book, chapter=chapter, paragraph=0, word=0)

        return Response({
            "chapter": progress.chapter,
            "paragraph": progress.paragraph,
            "word": progress.word,
            "timestamp": progress.timestamp,
        })
