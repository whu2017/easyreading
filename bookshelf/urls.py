# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from bookshelf.views import BookshelfView, BookshelfStatusView, BookshelfItemView


urlpatterns = [
    url(r'^$', BookshelfView.as_view(), name='bookshelf'),
    url(r'^/status$', BookshelfStatusView.as_view(), name='bookshelf_status'),
    url(r'^/book/(?P<book_id>[0-9]+)$', BookshelfItemView.as_view(), name='bookshelf_item'),
]
