# coding: utf-8
from rest_framework import serializers

from paradoxvault.models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = 'name'


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = 'name'


class SingleSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleSelection
        fields = ('question_type', 'subject', 'question', 'score', 'difficulty')


class MultiSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiSelection
        fields = ('question_type', 'subject', 'question', 'score', 'difficulty')


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = ('question_type', 'subject', 'question', 'score', 'difficulty')


class FillBlanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillBlanks
        fields = ('question_type', 'subject', 'question', 'score', 'difficulty')