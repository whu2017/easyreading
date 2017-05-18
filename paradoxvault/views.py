# coding: utf-8

from rest_framework import viewsets
from .models import *
from .serializers import *


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
