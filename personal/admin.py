# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from personal.models import Order, BuyRecord, DownloadRecord, ReadRecord


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'price', 'timestamp')


class BuyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')

admin.site.register(Order, OrderAdmin)
admin.site.register(BuyRecord, BuyRecordAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)

