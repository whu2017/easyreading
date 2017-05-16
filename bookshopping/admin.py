# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from bookshopping.models import (
    Category, Book, Bookshelf, Comment, Order, BuyRecord, DownloadRecord, ReadRecord,
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BookAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'author', 'price', 'score', 'total_chapter', 'allow_trial',
                    'trial_chapter', 'create_timestamp', 'update_timestamp')


class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'score', 'content', 'timestamp')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'price', 'timestamp')


class BuyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Bookshelf, BookshelfAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BuyRecord, BuyRecordAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)
