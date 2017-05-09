# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from check.views import CheckView


urlpatterns = [
    url(r'^$', CheckView.as_view(), name='view'),
]
