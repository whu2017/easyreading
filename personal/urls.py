# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from personal.views import (
    BalanceView, DepositListView, DepositItemView,
)


urlpatterns = [
    url(r'^/balance$', BalanceView.as_view(), name='balance'),
    url(r'^/deposit$', DepositListView.as_view(), name='deposit_list'),
    url(r'^/deposit/(?P<pk>[0-9]+)$', DepositItemView.as_view(), name='deposit_item'),
]
