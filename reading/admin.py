# -*- coding: utf-8 -*-

from django.contrib import admin

from reading.models import ReadingProgress, Bookmark


class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'chapter', 'paragraph', 'word', 'timestamp')


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'chapter', 'paragraph', 'word', 'timestamp')


admin.site.register(ReadingProgress, ReadingProgressAdmin)
admin.site.register(Bookmark, BookmarkAdmin)

