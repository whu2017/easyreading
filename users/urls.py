# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from users.views import LoginView, PermissionUpdateView, PermissionVerifyView


urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^permission/update$', PermissionUpdateView.as_view(), name='permission_update'),
    url(r'^permission/verify$', PermissionVerifyView.as_view(), name='permission_verify'),
]
