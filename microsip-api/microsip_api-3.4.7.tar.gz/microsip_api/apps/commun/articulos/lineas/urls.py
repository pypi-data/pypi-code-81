# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('lineas/$', views.lineas_articulos_view),
	path('linea/<int:id>/', views.linea_articulos_manageView),
    path('linea/', views.linea_articulos_manageView),
)