#encoding:utf-8
# from django.conf.urls import patterns, url
from django.urls import path,include
from .views import sucursales_view, sucursal_manageview, sucursal_delete
urlpatterns = (
    path('sucursales/', sucursales_view),
    path('sucursal/(<int:id>/', sucursal_manageview),
    path('sucursal_delete/(<int:id>/', sucursal_delete),
    path('sucursal/', sucursal_manageview),
)