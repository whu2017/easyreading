# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'email', 'phone', 'nickname', 'option_sync_progress', 'option_clean_cache',
        'option_display_progress', 'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
    )
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'phone', 'password'),
        }),
        ('个性设置', {
            'fields': ('nickname', 'signature'),
        }),
        ('个人选项', {
            'fields': (
                'option_sync_progress', 'option_clean_cache', 'option_display_progress',
                'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password',),
        }),
        ('个性设置', {
            'fields': ('nickname', 'signature'),
        }),
        ('个人选项', {
            'classes': ('wide',),
            'fields': (
                'option_sync_progress', 'option_clean_cache', 'option_display_progress',
                'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
            ),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('-id', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
