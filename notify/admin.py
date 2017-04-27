# -*- coding: utf-8 -*-

from django.contrib import admin

from notify.models import Notify, UserNotify, Subscription


class NotifyAdmin(admin.ModelAdmin):
    list_display = ('content', 'notify_type', 'target', 'target_type', 'action_type', 'sender', 'create_timestamp')


class UserNotifyAdmin(admin.ModelAdmin):
    list_display = ('user', 'notify', 'is_read', 'create_timestamp')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'target_type', 'action_type', 'create_timestamp')


admin.site.register(Notify, NotifyAdmin)
admin.site.register(UserNotify, UserNotifyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

