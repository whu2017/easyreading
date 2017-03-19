# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from app.user.models import UserProfile, UserOptions


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = '用户信息'
    verbose_name_plural = '用户信息'


class UserOptionsInline(admin.StackedInline):
    model = UserOptions
    can_delete = False
    verbose_name = '用户选项'
    verbose_name_plural = '用户选项'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserOptionsInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
