# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers


class ReadingProgressSerializer(serializers.Serializer):
    chapter = serializers.CharField()
    paragraph = serializers.IntegerField()
    word = serializers.IntegerField()
