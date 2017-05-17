# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from book.views import BookView, BookItemView, CommentListView, CommentItemView, CommentChildrenView, BuyView


urlpatterns = [
    url(r'^/book$', BookView.as_view(), name='book'),
    url(r'^/book/(?P<book_id>[0-9]+)$', BookItemView.as_view(), name='book_item'),
    url(r'^/book/(?P<book_id>[0-9]+)/comment$', CommentListView.as_view(), name='comment_list'),
    url(r'^/book/(?P<book_id>[0-9]+)/buy$', BuyView.as_view(), name='buy'),
    url(r'^/comment/(?P<comment_id>[0-9]+)$', CommentItemView.as_view(), name='comment_item'),
    url(r'^/comment/(?P<comment_id>[0-9]+)/children$', CommentChildrenView.as_view(), name='comment_children'),
]
