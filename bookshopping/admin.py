# -*- coding: utf-8 -*-

from django.contrib import admin

from bookshopping.models import *


class BookClassAdmin(admin.ModelAdmin):
    list_display = ('book_class_name',)


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ('book_class', 'title', 'price', 'data', 'cover', 'author', 'score', 'time', 'chapter')


class BookcaseAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user', 'comment_time', 'comment_contain', 'parent', 'comment_score')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user', 'buy_time', 'price')


class BuyRecordAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user', 'add_time')


class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user', 'add_time')


class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user', 'add_time')


admin.site.register(BookClass, BookClassAdmin)
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(Bookcase, BookcaseAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(BuyRecord, BuyRecordAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)
