from . import views

from django.urls import path


urlpatterns = [
    path('', views.AnswerView, name="Answer Api"),
]
