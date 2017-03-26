# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from user.views import LoginView


urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
]
