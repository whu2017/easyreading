# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from book.models import Category, Book, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BookAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'author', 'price', 'score', 'total_chapter', 'allow_trial',
                    'trial_chapter', 'create_timestamp', 'update_timestamp')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'score', 'content', 'timestamp')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)
