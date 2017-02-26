# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User


def index_view(request):
    users = User.objects.filter(is_superuser=True).order_by("id")
    branch = ""
    if len(users) > 0:
        branch = users[0].username
    return render(request, "index.html", {
        "branch": branch,
    })
