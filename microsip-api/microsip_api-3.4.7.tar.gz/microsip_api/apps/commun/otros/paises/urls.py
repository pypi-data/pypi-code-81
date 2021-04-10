# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('paises/', views.paises_view),
	path('pais/', views.pais_manageView),
    path('pais/<int:id>/', views.pais_manageView),
)