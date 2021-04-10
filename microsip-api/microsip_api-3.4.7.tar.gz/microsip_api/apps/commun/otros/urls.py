# from django.conf.urls import patterns, url, include
from django.urls import path,include

urlpatterns = (
	path('', include('microsip_web.apps.main.comun.otros.paises.urls', namespace='paises')),
	path('', include('microsip_web.apps.main.comun.otros.estados.urls', namespace='estados')),
	path('', include('microsip_web.apps.main.comun.otros.ciudades.urls', namespace='ciudades')),
	path('', include('microsip_web.apps.main.comun.otros.tipos_cambio.urls', namespace='tipo_cambio')),
)