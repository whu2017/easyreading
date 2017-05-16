# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from bookshelf.models import Bookshelf


class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_bought')


admin.site.register(Bookshelf, BookshelfAdmin)
