# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('grupos/', views.grupos_lineas_view),
	path('grupo/(<int:id>/', views.grupo_lineas_manageView),
    path('grupo/', views.grupo_lineas_manageView),
)