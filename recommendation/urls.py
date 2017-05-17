# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url

from recommendation.views import IndividuationView, RankView

urlpatterns = [
    url(r'^/individuation$', IndividuationView.as_view(), name='individuation'),
    url(r'^/rank$', RankView.as_view(), name='rank'),
]
