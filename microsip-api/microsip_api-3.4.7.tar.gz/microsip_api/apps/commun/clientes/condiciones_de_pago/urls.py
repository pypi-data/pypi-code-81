# from django.conf.urls import patterns, url
from django.urls import path,include
from django.views import generic
import views

urlpatterns = (
	path('condiciones_de_pago/', views.condiciones_de_pago_view),
	path('condicion_de_pago/<int:id>/', views.condicion_de_pago_manageView),
 	path('condicion_de_pago/', views.condicion_de_pago_manageView),
)