# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers
from django.db.models import ObjectDoesNotExist

from book.models import Book
from bookshelf.models import Bookshelf, BookshelfTimestamp
from personal.models import BuyRecord


class BookshelfQuerySerializer(serializers.Serializer):
    book_id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    is_bought = serializers.SerializerMethodField()

    class Meta:
        model = Bookshelf
        fields = ('id', 'book_id', 'title', 'author', 'cover', 'price', 'is_bought')

    def get_book_id(self, obj):
        return obj.book.pk

    def get_title(self, obj):
        return obj.book.title

    def get_author(self, obj):
        return obj.book.author

    def get_cover(self, obj):
        return obj.book.cover.url if obj.book.cover else ''

    def get_price(self, obj):
        return obj.book.price

    def get_is_bought(self, obj):
        return BuyRecord.objects.filter(user=obj.user, book=obj.book).exists()


class BookshelfPostSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('书籍不存在')
        return value


class BookshelfPutSerializer(serializers.Serializer):
    book_id = serializers.CharField()
