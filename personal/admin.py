# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from personal.models import Order, BuyRecord, ReadRecord, DepositRecord


class BuyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


class DepositRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'create_timestamp', 'modify_timestamp')

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'name', 'note', 'timestamp')


class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'timestamp')


admin.site.register(BuyRecord, BuyRecordAdmin)
admin.site.register(DepositRecord, DepositRecordAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ReadRecord, ReadRecordAdmin)
