# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from personal.views import (
    BalanceView, DepositListView, DepositItemView, BuyingView, OrderView, ReadView,
)


urlpatterns = [
    url(r'^/balance$', BalanceView.as_view(), name='balance'),
    url(r'^/buying$', BuyingView.as_view(), name='buying'),
    url(r'^/deposit$', DepositListView.as_view(), name='deposit'),
    url(r'^/deposit/(?P<pk>[0-9]+)$', DepositItemView.as_view(), name='deposit_item'),
    url(r'^/order$', OrderView.as_view(), name='order'),
    url(r'^/read$', ReadView.as_view(), name='read'),
]
