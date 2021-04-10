# from django.conf.urls import patterns, url, include
from django.urls import path,include

urlpatterns = (
	path('', include('microsip_web.apps.main.comun.articulos.articulos.urls', namespace='articulos')),
	path('', include('microsip_web.apps.main.comun.articulos.lineas.urls', namespace='lineas')),
	path('', include('microsip_web.apps.main.comun.articulos.grupos.urls', namespace='grupos')),
)