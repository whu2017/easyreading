# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from reading.views import ReadingProgressView, BookmarkView, BookmarkItemView, BookView, ChapterView


urlpatterns = [
    url(r'^book/(?P<book_id>[0-9]+)$', BookView.as_view(), name='book'),
    url(r'^book/(?P<book_id>[0-9]+)/chapter$', ChapterView.as_view(), name='chapter'),
    url(r'^book/(?P<book_id>[0-9]+)/progress$', ReadingProgressView.as_view(), name='reading_progress'),
    url(r'^book/(?P<book_id>[0-9]+)/bookmark$', BookmarkView.as_view(), name='bookmark'),
    url(r'^book/(?P<book_id>[0-9]+)/bookmark/(?P<bookmark_id>[0-9]+)$', BookmarkItemView.as_view(), name='bookmark_item'),
]
