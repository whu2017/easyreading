# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from book.models import Book


class RecommendationQuerySerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class RecommendationBookSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover', 'price')

    def get_cover(self, obj):
        return obj.cover.url if obj.cover else ''
