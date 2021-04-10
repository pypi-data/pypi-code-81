#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404,render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.conf import settings
from django.db.utils import DatabaseError
# user autentication
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import management
from .models import Empresa, Registry
from microsip_api.apps.cfdi.certificador.core import CertificadorSAT
from microsip_api.apps.cfdi.core import ClavesComercioDigital
from django_microsip_base.libs.models_base.models import ClienteUsuario,Cliente
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from microsip_api.comun.sic_db import first_or_none
from django.utils.crypto import get_random_string
import random
import string
from django.db import router, connections,connection
from .send_mail import send_mail_contrasena



def permission_required_view(request, template_name='administrador/permission_required.html'):
    return render(request, template_name, {})

@login_required( login_url = '/login/' )
def administrador_view( request, template_name = 'administrador/main.html' ):
    """ Lista de conexiones a carpetas ( Microsip Datos ). """
    c = {}
    return render( request, template_name, c)

@login_required( login_url = '/login/' )
def empresas_view( request, template_name = 'administrador/empresas/empresas.html' ):
    c = { 'empresas' : Empresa.objects.all() }
    return render( request, template_name, c)
    
@login_required( login_url = '/login/' )
def empresa_view( request, id=None, template_name = 'administrador/empresas/empresa.html' ):
    c = { 'empresa' : Empresa.objects.get(pk=id) }
    return render( request, template_name, c)

from django.core import serializers
import json
import os
class valida_datos_facturacion(TemplateView):

    def get(self, request, *args, **kwargs):
        rfc = Registry.objects.filter(padre__nombre='DatosEmpresa').get(nombre='Rfc').get_value().replace('-','').replace(' ','')
        certificados_mal=[]
        errors= []
        
        passwords = ClavesComercioDigital("%s\\comercio_digital_claves.xlsx"%settings.EXTRA_INFO['ruta_datos_facturacion'])
        if passwords.errors:
            if not errors:
                 errors += passwords.errors

        try:
            password = passwords[rfc]
        except KeyError:
            if not errors:
                errors.append("No se encontro la contraseña en archivo [comercio_digital_claves.xlsx].")


        sellos_path = '%s\\sellos\\'%settings.EXTRA_INFO['ruta_datos_facturacion']

        if not errors:
            try:
                carpetas = os.listdir(sellos_path)
            except WindowsError:
                errors.append("No se encontro carpeta [%s]"%sellos_path)
            else:
                certificador_sat = CertificadorSAT(settings.EXTRA_INFO['ruta_datos_facturacion'])
                errors_cert = certificador_sat.certificar(empresa_folder_name= rfc)
                if errors_cert:
                    certificados_mal.append(rfc)
                    errors.append(errors_cert)



        data = {
            'certificados_mal':certificados_mal,   
            'errors':errors,
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')

from django.db import connections
class sincronizar_basedatos(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            basedatos_activa = request.session[ 'selected_database' ]
        if basedatos_activa == '':
            return HttpResponseRedirect( '/select_db/' )
        else:
            conexion_activa_id = request.session[ 'conexion_activa' ]
            
        conexion_name = "%02d-%s"%( conexion_activa_id, basedatos_activa )
        
        # Campos nuevos en tablas
        #management.call_command('makemigrations')
        
        sincronizar_tablas( conexion_name = conexion_name )

        management.call_command( 'migrate','--noinput',app_label='models_base',database = conexion_name )
        errors = []
        data = {
            'errors':errors,
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')

def sincronizar_tablas(conexion_name):
    c = connections[ conexion_name ].cursor()
    try:
        c.execute("DELETE FROM DJANGO_CONTENT_TYPE;")
    except DatabaseError:
        pass
    else:
        import importlib

        for plugin in settings.EXTRA_APPS:
            plugin_procedures = None
            try:
                plugin_procedures_module = importlib.import_module(plugin['app']+'.procedures')
            except ImportError:
                pass
            else:
                plugin_procedures = plugin_procedures_module.procedures

            if plugin_procedures:
                for procedure in plugin_procedures.keys():
                    c.execute( plugin_procedures[procedure] )
                    c.execute('EXECUTE PROCEDURE %s;'%procedure)
                    c.execute('DROP PROCEDURE %s;'%procedure)

def crear_usuarios_clientes(request):
    if request.GET.get('cliente_id'):
        cliente_id=request.GET.get('cliente_id')
    cliente=first_or_none(Cliente.objects.filter(id=cliente_id))
    inf_cliente=first_or_none(ClienteDireccion.objects.filter(cliente=cliente,es_ppal='S'))
    password=""
    if inf_cliente.rfc_curp:
        try:
            print("******* try")
            usuario = User.objects.get(username__exact=inf_cliente.rfc_curp)
            print(usuario)
            password=""
        except ObjectDoesNotExist:
            print("******* except")
            rfc=(inf_cliente.rfc_curp).replace("-","")
            rfc=rfc.replace(" ","")
            print(rfc)
            password = randomString(10)
            if inf_cliente.email:
                guardar=str(password)+","+inf_cliente.email
            else:
                guardar=str(password)           
            
            user = User.objects.create_user(username = rfc, password=password,first_name=cliente.nombre,last_name='usuario_externo',email=guardar)
            usuario_cliente=ClienteUsuario.objects.get_or_create(cliente=cliente,usuario=user.id)

            
            using = router.db_for_write(Articulo)
            c = connections[using].cursor()

            query = "CREATE USER %s PASSWORD '%s' active"%(rfc,password)
            c.execute(query)
            c.execute('COMMIT')
    
    data={
        "password":password,
    }


    return HttpResponse(json.dumps(data), content_type='application/json')

def usuario_cliente(request):
    clientes=Cliente.objects.filter(estatus='A')

    page = request.GET.get('page')

    form_busqueda=FilterForm(request.POST or None)
    
    if form_busqueda.is_valid():
        busqueda=form_busqueda.cleaned_data['busqueda']
        print(busqueda)
        if busqueda:
            clientes=clientes.filter(nombre__icontains=busqueda)

    paginator = Paginator(clientes, 50) 
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        
        clientes = paginator.page(1)
    except EmptyPage:
        
        clientes = paginator.page(paginator.num_pages)

    for cliente in clientes:
        cliente_usuario=first_or_none(ClienteUsuario.objects.filter(cliente=cliente))
        if cliente_usuario:
            client_usuario=first_or_none(User.objects.filter(id=cliente_usuario.usuario))
            cliente.usuario=client_usuario

    clientes_usuario=User.objects.all()
    
    context = {
        "clientes_usuario":clientes_usuario,
        "clientes":clientes,
        "form_busqueda":form_busqueda,
    }
    
    return render(request, 'administrador/usuarios_clientes.html', context)


def cambiar_contrasena(request):
    articulos=None
    username=request.user.username
    form_initial={
        'usuario':username,
        'anterior_contrasena':None,
        'nueva_contrasena':None,
    }
    mensaje=None
    form=UsuarioForm(request.POST or None,initial=form_initial)
    
    if form.is_valid():
        try:
            usuario=form.cleaned_data['usuario']
            anterior_contrasena=form.cleaned_data['anterior_contrasena']    
            nueva_contrasena=form.cleaned_data['nueva_contrasena']
            usuario=User.objects.get(username__exact=usuario)
            usuario.set_password(nueva_contrasena)
            email_separar=usuario.email.split(",")
            contrasena=email_separar[0]
            correos=email_separar[1]
            usuario.email=nueva_contrasena
            usuario.save()
            using = router.db_for_write(Articulo)
            c = connections[using].cursor()
            query = "ALTER USER %s PASSWORD '%s'"%(username,nueva_contrasena)
            c.execute(query)
            c.execute('COMMIT')
            mensaje=u"Cambio de contraseña exitoso"
        except Exception as e:
            mensaje=u"Ocurrio un error al cambiar la contraseña, intentelo mas tarde o contacte con el administrador"
    context={
        'form':form,
        'mensaje':mensaje,
    }
    return render(request, 'administrador/cambiar_contraseña.html', context)

def recuperar_contrasena(request):
    mensaje=""
    if request.method=='POST' and 'enviar' in request.POST:
        try:
            usuario=first_or_none(User.objects.filter(id=request.POST["id_usuario"]))
            print(usuario.email)
            email_separar=usuario.email.split(",")
            contrasena=email_separar[0]
            if len(email_separar) >1:
                correos=email_separar[1]
            else:
                correos=None
            print(contrasena)
            print(correos)
            if correos:
                destinatarios=(correos).split(';')
                email = DatabaseSucursal.objects.get(name='SIC_Usuario_externo_Email')
                password = DatabaseSucursal.objects.get(name='SIC_Usuario_externo_Password')
                servidor_correo = DatabaseSucursal.objects.get(name='SIC_Usuario_externo_Servidro_Correo')
                puerto = DatabaseSucursal.objects.get(name='SIC_Usuario_externo_Puerto')
                print(usuario,email,password,servidor_correo,puerto)
                file=None
                contenido=u"<html lang='es'><p>ACCESO DE CUENTA EN LLANTAS Y SERVICIOS EL PINO PARA %s</p><p><strong>USUARIO: %s</strong></p><p><strong>CONTRSEÑA: %s</strong></p></html>"%(usuario.first_name,usuario.username,str(contrasena))
                nombre=""
                data={}
                bandera=send_mail_contrasena(servidor_correo.empresa_conexion,puerto.empresa_conexion,email.empresa_conexion,password.empresa_conexion,destinatarios,"CONTRSEÑA DE ACCESO",contenido,file,nombre)
                mensaje=u"Reenvio correcto"
            else:
                mensaje=u"No hay email al que enviar correo" 
        except Exception as e:
            print(e)
            mensaje=u"Ocurrio un error al enviar la contraseña, intentelo mas tarde o contacte con el administrador"


    print(mensaje)
    context={
        'mensaje':mensaje,
    }
    return render(request, 'administrador/recuperar_contrasena.html', context)

def find_user(request):
    usuario=None
    if request.GET.get('nombre_cliente'):
        nombre_cliente=request.GET.get('nombre_cliente')
        try:
            usuario = User.objects.get(username__exact=nombre_cliente)
        except ObjectDoesNotExist:
            usuario=None
    data={}

    if usuario:
        data["mensaje"]="Si"
        data["id_usuario"]=str(usuario.id)
    else:
        data["mensaje"]="No"
        data["id_cliente"]=""

    return HttpResponse(json.dumps(data), content_type='application/json')

def enviar_correo(request):
    id_crm=request.GET['id']
    pedido=Pedidos_Crm.objects.get(id=id_crm)
    venta=VentasDocumento.objects.get(folio=pedido.folio)
    cliente=ClienteDireccion.objects.get(cliente=venta.cliente)
    destinatarios=(cliente.email).split(';')
    email= Registry.objects.get( nombre = 'SIC_Usuario_externo_Email').get_value()
    password= Registry.objects.get( nombre = 'SIC_Usuario_externo_Password').get_value()
    servidor_correo= Registry.objects.get( nombre = 'SIC_Usuario_externo_Servidro_Correo').get_value()
    puerto= Registry.objects.get( nombre = 'SIC_Usuario_externo_Puerto').get_value()
    #superkarelyrubio@hotmail.com
    nombre=none_cero(venta.folio)+".pdf"
    pdf=create_pdf(venta.id)
    destination = Registry.objects.get( nombre = 'SIC_Usuario_externo_Url_Pdf_Destino').get_value()
    file=destination+"\\" + nombre
    data={}
    bandera=send_mail_orden(servidor_correo,puerto,email,password,destinatarios,"Nota de servicio","<p>Servicios de Ingenieria</p>",file,nombre)
    if bandera:
        pedido.envio_correo=1
        print(pedido.envio_correo)
        pedido.save()
        data["mensaje"]="Correo Enviado"
        print(data)
    else:
        data["mensaje"]="Hubo un error al enviar el correo"
        print(data)

    return HttpResponse(json.dumps(data), content_type='application/json')

def enviar_contrasena(request,id):
    cliente=ClienteDireccion.objects.get(cliente__id=id)
    usuario_cliente=first_or_none(ClienteUsuario.objects.filter(cliente__id=id))
    usuario=first_or_none(User.objects.filter(id=usuario_cliente.usuario))
    if cliente.email:
        destinatarios=(cliente.email).split(';')
    else:
        destinatarios=None
    datos_empresa = Registry.objects.get(nombre='DatosEmpresa')
    datos_empresa = Registry.objects.filter(padre=datos_empresa)
    nombre=datos_empresa.get(nombre='Nombre').get_value()
    email= Registry.objects.get( nombre = 'SIC_Usuario_externo_Email').get_value()
    password= Registry.objects.get( nombre = 'SIC_Usuario_externo_Password').get_value()
    servidor_correo= Registry.objects.get( nombre = 'SIC_Usuario_externo_Servidro_Correo').get_value()
    puerto= Registry.objects.get( nombre = 'SIC_Usuario_externo_Puerto').get_value()
    #superkarelyrubio@hotmail.com
    if usuario.email:
        email_separar=usuario.email.split(",")
        if len(email_separar) > 1:
            contrasena=email_separar[0]
            correos=email_separar[1]
        else:
            contrasena=email_separar[0]
            correos=None
    else:
        contrasena=None
        correos=None    
    file=None
    contenido=u"<html lang='es'><p>ACCESO DE CUENTA EN LLANTAS Y SERVICIOS EL PINO PARA %s</p><p><strong>USUARIO: %s</strong></p><p><strong>CONTRSEÑA: %s</strong></p></html>"%(cliente.cliente.nombre,usuario.username,str(contrasena))
    nombre=""
    data={}
    bandera=send_mail_contrasena(servidor_correo,puerto,email,password,destinatarios,"CONTRSEÑA DE ACCESO",contenido,file,nombre)
    if bandera:
        data["mensaje"]="Correo Enviado"
        print(data)
    else:
        data["mensaje"]="Hubo un error al enviar el correo"
        print(data)

    return HttpResponse(json.dumps(data), content_type='application/json')

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def preferencias(request):
    padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))

    if not Registry.objects.filter( nombre = 'SIC_Usuario_externo_BD_Automatica' ).exists():
        Registry.objects.create(
            nombre = 'SIC_Usuario_externo_BD_Automatica',
            tipo = 'V',
            padre = padre,
            valor= '',
        )
    if not Registry.objects.filter( nombre = 'SIC_Usuario_externo_Email' ).exists():
            Registry.objects.create(
                nombre = 'SIC_Usuario_externo_Email',
                tipo = 'V',
                padre = padre,
                valor= '',
            )
    if not Registry.objects.filter( nombre = 'SIC_Usuario_externo_Password' ).exists():
            Registry.objects.create(
                nombre = 'SIC_Usuario_externo_Password',
                tipo = 'V',
                padre = padre,
                valor= '',
            )
    if not Registry.objects.filter( nombre = 'SIC_Usuario_externo_Servidro_Correo' ).exists():
            Registry.objects.create(
                nombre = 'SIC_Usuario_externo_Servidro_Correo',
                tipo = 'V',
                padre = padre,
                valor= '',
            )
    if not Registry.objects.filter( nombre = 'SIC_Usuario_externo_Puerto' ).exists():
            Registry.objects.create(
                nombre = 'SIC_Usuario_externo_Puerto',
                tipo = 'V',
                padre = padre,
                valor= '',
            )

    base_datos_automatica=Registry.objects.get(nombre='SIC_Usuario_externo_BD_Automatica').get_value()


    email= Registry.objects.get( nombre = 'SIC_Usuario_externo_Email').get_value()
    password= Registry.objects.get( nombre = 'SIC_Usuario_externo_Password').get_value()
    servidor_correo= Registry.objects.get( nombre = 'SIC_Usuario_externo_Servidro_Correo').get_value()
    puerto= Registry.objects.get( nombre = 'SIC_Usuario_externo_Puerto').get_value()


    
    form_initial=None
    
    form_initial = {
            'base_datos_automatica':base_datos_automatica,
            'email':email,
            'password':password,
            'servidor_correo':servidor_correo,
            'puerto':puerto,
    }

    form = PreferenciasManageForm(request.POST or None,initial=form_initial,conexion_activa = request.session['conexion_activa'])
    if form.is_valid():
        form.save()
 
    context = {
        'form': form,
    }
    return render(request, 'administrador/preferencias.html', context)


def solicitar_usuario(request):
    pass