# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('clientes/', views.clientes_view),
	path('cliente/<int:id>/', views.cliente_manageView),
    path('cliente/', views.cliente_manageView),
)