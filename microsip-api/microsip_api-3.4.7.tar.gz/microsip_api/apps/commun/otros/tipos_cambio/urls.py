# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('tipos_cambio/', views.tipos_cambio_view),
)