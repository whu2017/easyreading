# -*- coding: utf-8 -*-

from django.contrib import admin

from transform.models import Transform


class TransformAdmin(admin.ModelAdmin):
    list_display = ('origin', 'book', 'status', 'error_message')
    exclude = ('book', 'status', 'error_message')

    def suit_cell_attributes(self, obj, column):
        if column == 'origin':
            return {'style': 'word-break:break-all;width:250px'}
        elif column == 'book':
            return {'style': 'word-break:break-all;width:250px'}
        elif column == 'status':
            return {'style': 'word-break:break-all;width:100px'}
        elif column == 'error_message':
            return {'style': 'word-break:break-all;width:250px'}


admin.site.register(Transform, TransformAdmin)
