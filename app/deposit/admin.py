# -*- coding: utf-8 -*-

from django.contrib import admin

from app.deposit.models import Deposit


class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'create_timestamp', 'modify_timestamp')

    def has_add_permission(self, request):
        return False


admin.site.register(Deposit, DepositAdmin)
