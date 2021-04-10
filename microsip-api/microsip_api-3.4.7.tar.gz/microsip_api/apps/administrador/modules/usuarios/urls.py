#encoding:utf-8
# from django.conf.urls import patterns, url
from django.urls import path,include
from . import views
urlpatterns =(
    path('usuarios/', views.usuarios_view),
    path('usuario/<int:id>/', views.usuario_manageview),
    path('change_user_permission/', views.change_user_permission),
    path('get_apppsermissions/', views.get_apppsermissions),
)
