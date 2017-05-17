# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from deposit.views import RecordListView, RecordItemView, BalanceView


urlpatterns = [
    url(r'^/balance$', BalanceView.as_view(), name='balance'),
    url(r'^/record$', RecordListView.as_view(), name='record_list'),
    url(r'^/record/(?P<pk>[0-9]+)$', RecordItemView.as_view(), name='record_item'),
]
