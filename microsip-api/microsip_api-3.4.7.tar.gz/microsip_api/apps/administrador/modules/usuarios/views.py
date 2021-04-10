#encoding:utf-8
from . import forms
from ....config.models import Usuario
from django.contrib.auth.models import User,Permission
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponse
import json
from microsip_api.comun.sic_db import first_or_none
import random
import string
from microsip_api.core.permissions import Permissions

# permission = Permissions()
# permission.get_permissions()


def getInstalledApps():
    installed_apps = []
    for app_key in settings.EXTRA_MODULES:
        installed_apps.append(app_key)
    return installed_apps


@login_required(login_url='/login/')
def usuarios_view(request, template_name='administrador/usuarios/usuarios.html'):
    c = {'usuarios': Usuario.objects.all(), }
    return render(request,template_name, c)


def get_pass():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set*12, 12))


@login_required(login_url='/login/')
def usuario_manageview(request, id=None, template_name='administrador/usuarios/usuario.html'):
    # usuario = Usuario.objects.get(id=id)
    django_user = Usuario.objects.get(id=id)
    #usuario=User.objects.get(username=django_user.nombre)
    permisos=Permission.objects.all()
    #permisos_usuario=
    
    c = {'django_user': django_user, 'permisos':permisos,}
    return render(request,template_name, c)


def change_user_permission(request):
    """
    change permission
    """
    print("change")
    permiso_id = request.GET['permiso_id']
    django_user_id = request.GET['django_user_id']
    checked = request.GET['checked'] == u'true'
    django_user = Usuario.objects.get(id=django_user_id)
    usuario=User.objects.get(username=django_user.nombre)

    permiso = Permission.objects.get(id=permiso_id)
    if checked:
        print(permiso)
        usuario.user_permissions.add(permiso)
    else:
        usuario.user_permissions.remove(permiso)

    data = json.dumps({})
    return HttpResponse(data, content_type='application/json')


def get_apppsermissions(request):
    """
    get apps permissions
    """
    django_user_id = request.GET['django_user_id']
    django_user = Usuario.objects.get(id=django_user_id)
    username=request.user
    print(username)
    print(django_user)
    from microsip_api.core.permissions import Permissions

    permission = Permissions(username=username,dj_user=django_user)
    data = json.dumps(permission.get_permissions())
    return HttpResponse(data, content_type='application/json')
