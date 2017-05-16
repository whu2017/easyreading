# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from bookshopping.models import BookClass

class BookView(APIView):