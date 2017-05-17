# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from book.models import Book, Category, Comment


class BookQuerySerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover', 'price')
        depth = 0


class BookItemSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'category_id', 'category_name', 'author', 'cover', 'introduction', 'price',
                  'score', 'total_chapter', 'latest_chapter_text', 'allow_trial', 'trial_chapter',
                  'create_timestamp', 'update_timestamp')

    def get_category_id(self, obj):
        return obj.category.pk

    def get_category_name(self, obj):
        return obj.category.name
