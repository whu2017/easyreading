# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers
from django.db.models import ObjectDoesNotExist

from book.models import Book
from personal.models import BuyRecord
from lib.parser.epub import parse_structure


class ChapterSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        identifier = value
        user = self.context['request'].user
        book_id = self.context['book_id']
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('该章节所对应的书籍不存在')

        chapter_exist = False
        chapter_index = 0
        structure = parse_structure(book.resource.final.path)
        for index, item in enumerate(structure):
            if item.get('identifier') == identifier:
                chapter_exist = True
                chapter_index = index
                break
        if not chapter_exist:
            raise serializers.ValidationError('该章节不存在')

        if BuyRecord.objects.filter(user=user, book=book).exists():
            return identifier

        if (not book.allow_trial) or (chapter_index + 1 > book.trial_chapter):
            raise serializers.ValidationError('该章节需付费阅读，请购买该书籍')
        return identifier


class ReadingProgressSerializer(serializers.Serializer):
    chapter = serializers.CharField()
    paragraph = serializers.IntegerField(min_value=0)
    word = serializers.IntegerField(min_value=0)


class BookmarkSerializer(serializers.Serializer):
    chapter = serializers.CharField()
    paragraph = serializers.IntegerField(min_value=0)
    word = serializers.IntegerField(min_value=0)
    detail = serializers.CharField()


class BookmarkGetSerializer(serializers.Serializer):
    detail_length = serializers.IntegerField(min_value=1, max_value=50, default=20)
