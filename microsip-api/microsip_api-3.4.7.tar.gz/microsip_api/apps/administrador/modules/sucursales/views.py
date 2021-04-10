#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from microsip_api.comun.sic_db import get_conecctionname

@login_required( login_url = '/login/' )
def sucursales_view( request, template_name = 'administrador/sucursales/sucursales.html' ):
    """ Lista de sucursales de empresa. """
    connection_name = get_conecctionname(request.session)
    c = { 'sucursales' : DatabaseSucursal.objects.filter(empresa_conexion=connection_name) }
    return render(request, template_name, c )

@login_required(login_url='/login/')
def sucursal_manageview( request, id = None, template_name = 'administrador/sucursales/sucursal.html' ):
    """ Sucursal manejador """
    message = ''
    initial_form = None
    if id:
        sucursal = get_object_or_404( DatabaseSucursal, pk = id)
    else:
        sucursal =  DatabaseSucursal()

    form = DatabaseSucursalForm(request.POST or None, instance = sucursal)

    if form.is_valid():
        sucursal_form =form.save(commit=False)
        sucursal_form.empresa_conexion = get_conecctionname(request.session)
        conexion_id, empresa = sucursal_form.sucursal_conexion.split('-')
        conexion = ConexionDB.objects.get(pk=int(conexion_id))
        database_conexion_name = "%s-%s"%(conexion.nombre, empresa)
        sucursal_form.sucursal_conexion_name = database_conexion_name
        sucursal_form.save()

        return HttpResponseRedirect( '/administrador/sucursales/' )

    c = { 'form' : form, }
    return render(request, template_name, c )

@login_required(login_url='/login/')
def sucursal_delete( request, id = None):
    """ 
    Eliminar una sucursal.
    """
    sucursal = DatabaseSucursal.objects.get(pk= id)
    sucursal.delete()
    return HttpResponseRedirect( '/administrador/sucursales/' )

