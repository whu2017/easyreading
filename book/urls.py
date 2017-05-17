# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from book.views import BookView, BookItemView


urlpatterns = [
    url(r'^book$', BookView.as_view(), name='book'),
    url(r'^book/(?P<book_id>[0-9]+)$', BookItemView.as_view(), name='book_item'),
]
