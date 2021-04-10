# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('articulos/', views.articulos_view),
	path('articulos/<int:carpeta>/', views.articulos_view),
	path('articulo/<int:id>/', views.articulo_manageview),
    path('articulo/', views.articulo_manageview),
)