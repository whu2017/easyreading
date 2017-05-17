# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from personal.models import DepositRecord


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
