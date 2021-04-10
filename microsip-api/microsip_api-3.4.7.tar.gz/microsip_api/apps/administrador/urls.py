# from django.conf.urls import patterns, url, include
from django.urls import path,include
from .views import *
from microsip_api.apps.administrador import views
urlpatterns = (
	path('',views.administrador_view),
	path('empresas/',views.empresas_view),
	path('empresa/<int:id>/',views.empresa_view),
	path('valida_datos_facturacion/', valida_datos_facturacion.as_view()),
	path('permission_required/', permission_required_view),
	path('sincronizar_basedatos/', sincronizar_basedatos.as_view()),
	path('crear_usuarios_clientes/', crear_usuarios_clientes),
	path('usuario_cliente/', usuario_cliente),
	path('cambiar_contrasena/', cambiar_contrasena),
	path('recuperar_contrasena/', recuperar_contrasena),
	path('find_user/', find_user),
	path('solicitar_usuario/', solicitar_usuario),
	path('preferencias/', preferencias),
	path('enviar_contrasena/<int:id>/', enviar_contrasena),
	path('', include('microsip_api.apps.administrador.modules.sucursales.urls')),
	path('', include('microsip_api.apps.administrador.modules.usuarios.urls')),
)