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


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    sub_comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'user_nickname', 'user_avatar', 'content', 'score', 'timestamp', 'sub_comment_count')
        depth = 0

    def get_user_id(self, obj):
        return obj.user.pk

    def get_user_nickname(self, obj):
        user = obj.user
        if user.nickname:
            return user.nickname
        if user.phone:
            return user.phone.replace(user.phone[3:7], '*'*4)
        return user.email

    def get_user_avatar(self, obj):
        return obj.user.avatar.url if obj.user.avatar else ''

    def get_sub_comment_count(self, obj):
        return obj.children.count()
