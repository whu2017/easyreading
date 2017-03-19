# -*- coding: utf-8 -*-

from django.contrib import admin

from app.transform.models import Transform


class TransformAdmin(admin.ModelAdmin):
    list_display = ('pk', 'book', 'status', 'error_message')
    exclude = ('book', 'status', 'error_message')


admin.site.register(Transform, TransformAdmin)
