# coding: utf-8
from rest_framework import serializers

from paradoxvault.models import *

from django.core.exceptions import ObjectDoesNotExist


class QuestionQuerySerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)


class QuestionBankListSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    class Meta:
        model = QuestionBank
        fields = ('id', 'title', 'author', 'cover', 'price')
        depth = 0

    def get_cover(self, obj):
        return obj.cover.url if obj.cover else ''


class QuestionBankItemSerializer(serializers.ModelSerializer):
    subject_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = QuestionBank
        fields = ('id', 'title', 'subject', 'author', 'cover', 'introduction', 'price',
                  'score', 'total_chapter', 'create_timestamp', 'update_timestamp')

    def get_subject_id(self, obj):
        return obj.Subject.pk

    def get_subject_name(self, obj):
        return obj.Subject.name


# class SelectionSerializer(serializers.ModelSerializer):
#     SelectionOptions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Selection
#         fields = ('id', 'question_type', 'question', 'grade', 'difficulty', 'option')
#         depth = 1
#
#     def get_options(self, obj):
#         return obj.children.values('option')


class CommentDisplaySerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    sub_comment_count = serializers.SerializerMethodField()

    class Meta:
        model = QuestionComment
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


class CommentPostSerializer(serializers.Serializer):
    score = serializers.FloatField(min_value=0, max_value=5)
    content = serializers.CharField()
    parent_id = serializers.IntegerField()

    def validate_parent_id(self, value):
        if value == 0:
            return value

        try:
            QuestionComment.objects.get(pk=value)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('父评论不存在')
        return value
