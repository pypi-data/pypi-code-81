# from django.conf.urls import patterns, url, include
from django.urls import path,include

urlpatterns = (
	path('', include('microsip_web.apps.main.comun.clientes.clientes.urls', namespace='Clientes')),
	path('', include('microsip_web.apps.main.comun.clientes.condiciones_de_pago.urls', namespace='condiciones_de_pago')),
)