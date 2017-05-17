# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from bookshelf.models import Bookshelf, BookshelfTimestamp


class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'create_timestamp')


class BookshelfTimestampAdmin(admin.ModelAdmin):
    list_display = ('user', 'update_timestamp')


admin.site.register(Bookshelf, BookshelfAdmin)
admin.site.register(BookshelfTimestamp, BookshelfTimestampAdmin)