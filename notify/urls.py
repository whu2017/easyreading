# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from notify.views import NotifyItemView, NotifyListView


urlpatterns = [
    url(r'^$', NotifyListView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', NotifyItemView.as_view(), name='item'),
]
