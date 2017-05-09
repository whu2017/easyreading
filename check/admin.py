# -*- coding: utf-8 -*-

from django.contrib import admin

from check.models import Check


class CheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_timestamp')

    def has_add_permission(self, request):
        return False


admin.site.register(Check, CheckAdmin)