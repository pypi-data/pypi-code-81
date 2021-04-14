# -*- coding: utf-8 -*-

from django.urls import path

from .views import JSNLogView

urlpatterns = [
    path(r'', JSNLogView.as_view()),
]
