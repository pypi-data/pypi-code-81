# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('impuestos/', views.impuestos_view),
	path('impuesto/', views.impuesto_manageView),
    path('impuesto/<int:id>/', views.impuesto_manageView),
)