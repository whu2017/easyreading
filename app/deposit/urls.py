# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from app.deposit.views import RecordListView, RecordItemView


urlpatterns = [
    url(r'^record$', RecordListView.as_view(), name='record_list'),
    url(r'^record/(?P<pk>[0-9]+)/$', RecordItemView.as_view(), name='record_item'),
]
