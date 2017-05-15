# coding: utf-8
from rest_framework import serializers

from paradoxvault import models


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('subject', 'type', 'ID')

