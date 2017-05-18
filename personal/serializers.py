# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from personal.models import DepositRecord, Order, BuyRecord, ReadRecord


class BuyItemSerializer(serializers.ModelSerializer):
    book_id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = BuyRecord
        fields = ('id', 'book_id', 'title', 'author', 'cover', 'price', 'timestamp')

    def get_book_id(self, obj):
        return obj.book.pk

    def get_title(self, obj):
        return obj.book.title

    def get_author(self, obj):
        return obj.book.author

    def get_cover(self, obj):
        return obj.book.cover.url if obj.book.cover else ''


class DepositPostSerializer(serializers.Serializer):
    amount = serializers.FloatField()

    def validate_amount(self, value):
        if value <= 0.0:
            raise serializers.ValidationError('充值金额必须为正数')
        return value


class DepositItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositRecord
        fields = ('id', 'amount', 'status', 'create_timestamp', 'modify_timestamp')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'amount', 'name', 'note', 'timestamp')


class ReadSerializer(serializers.ModelSerializer):
    book_id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'book_id', 'title', 'author', 'cover')

    def get_book_id(self, obj):
        return obj.book.pk

    def get_title(self, obj):
        return obj.book.title

    def get_author(self, obj):
        return obj.book.author

    def get_cover(self, obj):
        return obj.book.cover.url if obj.book.cover else ''