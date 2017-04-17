# -*- coding: utf-8 -*-

from django.contrib import admin

from app.deposit.models import Deposit


class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'create_timestamp', 'modify_timestamp')


admin.site.register(Deposit, DepositAdmin)
