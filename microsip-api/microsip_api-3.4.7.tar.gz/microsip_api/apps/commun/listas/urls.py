# from django.conf.urls import patterns, url, include
from django.urls import path,include

urlpatterns = (
	path('', include('microsip_web.apps.main.comun.listas.impuestos.urls', namespace='listas')),
)