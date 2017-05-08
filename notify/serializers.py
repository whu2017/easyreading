# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from notify.models import Notify, UserNotify


class UserNotifyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotify
        fields = ('id', 'is_read', 'notify', 'create_timestamp')
        depth = 1
