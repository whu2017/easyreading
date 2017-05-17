# -*- coding: utf-8 -*-

"""easyreading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from index.views import index_view


urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^notify/', include('notify.urls', namespace='notify')),
    url(r'^check/', include('check.urls', namespace='check')),
    url(r'^deposit/', include('deposit.urls', namespace='deposit')),
    url(r'^reading/', include('reading.urls', namespace='reading')),
    url(r'^bookshopping/', include('book.urls', namespace='book')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
