# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('estados/', views.estados_view),
	path('estado/', views.estado_manageView),
 	path('estado/<int:id>/', views.estado_manageView),
)