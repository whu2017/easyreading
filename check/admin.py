# -*- coding: utf-8 -*-

from django.contrib import admin

from check.models import Check


class CheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_timestamp')


admin.site.register(Check, CheckAdmin)

