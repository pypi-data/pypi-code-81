# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns =(
	path('ciudades/', views.ciudades_view),
	path('ciudad/', views.ciudad_manageView),
 	path('ciudad/<int:id>/', views.ciudad_manageView),
)