# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^/questionbank$', QuestionBankView.as_view()),
    url(r'^/questionbank/(?P<questionbank_id>[0-9]+)$', QuestionBankItemView.as_view()),
    url(r'^/questionbank/(?P<questionbank_id>[0-9]+)/comment$', QuestionCommentListView.as_view()),
    url(r'^/comment/(?P<comment_id>[0-9]+)$', QuestionCommentItemView.as_view()),
    url(r'^/comment/(?P<comment_id>[0-9]+)/children$', QuestionCommentChildrenView.as_view()),
    url(r'^/questionbank/(?P<questionbank_id>[0-9]+)/selection$', SelectionView.as_view()),
]
