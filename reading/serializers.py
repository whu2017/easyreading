# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers


class ReadingProgressSerializer(serializers.Serializer):
    chapter = serializers.CharField()
    paragraph = serializers.IntegerField(min_value=0)
    word = serializers.IntegerField(min_value=0)


class BookmarkSerializer(serializers.Serializer):
    chapter = serializers.CharField()
    paragraph = serializers.IntegerField(min_value=0)
    word = serializers.IntegerField(min_value=0)


class BookmarkGetSerializer(serializers.Serializer):
    detail_length = serializers.IntegerField(min_value=1, max_value=50, default=20)
