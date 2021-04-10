# Django
from django import forms 
from datetime import date
from django.forms.models import inlineformset_factory
from dal import autocomplete
from django_select2 import forms as s2forms
from .models import *
from django_microsip_base.libs.models_base.models import VentasDocumentoDetalle, VentasDocumento, Articulo, Cliente, Almacen, ClienteDireccion, CondicionPago, Vendedor,Registry
from django.conf import settings
from django_microsip_base.libs.models_base.models import ConexionDB,DatabaseSucursal
import fdb, os

class FilterForm(forms.Form):
	busqueda=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','place-holder':'Ingrese criterio de busqueda'}), required=False)

class PreferenciasManageForm(forms.Form):
	def __init__(self,*args,**kwargs):
		empresas=[]
		conexion_activa = kwargs.pop('conexion_activa')
		if conexion_activa != '':
			conexion_activa = ConexionDB.objects.get(pk=conexion_activa)
		else:
			conexion_activa = None

		if conexion_activa:
			db= fdb.connect(host=conexion_activa.servidor, user= conexion_activa.usuario, password=conexion_activa.password, database="%s\System\CONFIG.FDB"%conexion_activa.carpeta_datos)
			c = db.cursor()
			query = u"SELECT EMPRESAS.nombre_corto FROM EMPRESAS order by nombre_corto"
			c.execute(query)
			empresas_rows = c.fetchall()
			for empresa in empresas_rows:
				try:
					empresa = u'%s'%empresa[0]
				except UnicodeDecodeError:
					pass
				else:
					empresa_option = [empresa, empresa]
					empresas.append(empresa_option)
		
		super(PreferenciasManageForm,self).__init__(*args,**kwargs)
        
		self.fields['base_datos_automatica']=forms.ChoiceField(choices=empresas,widget=forms.Select(attrs={'class': 'form-control'}))
		self.fields['email']=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
		self.fields['password']=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
		self.fields['servidor_correo'] = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
		self.fields['puerto']=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}),)




	def save(self, *args, **kwargs):
		base_datos_automatica = Registry.objects.get( nombre = 'SIC_Usuario_externo_BD_Automatica')
		base_datos_automatica.valor = self.cleaned_data['base_datos_automatica']
		base_datos_automatica.save()
		email = Registry.objects.get( nombre = 'SIC_Usuario_externo_Email')
		email.valor = self.cleaned_data['email']
		email.save()
		password = Registry.objects.get( nombre = 'SIC_Usuario_externo_Password')
		password.valor = self.cleaned_data['password']
		password.save()
		servidor_correo = Registry.objects.get( nombre = 'SIC_Usuario_externo_Servidro_Correo')
		servidor_correo.valor = self.cleaned_data['servidor_correo']
		servidor_correo.save()
		puerto = Registry.objects.get( nombre = 'SIC_Usuario_externo_Puerto')
		puerto.valor = self.cleaned_data['puerto']
		puerto.save()

		DatabaseSucursal.objects.get_or_create(name='usuario_externo',empresa_conexion=base_datos_automatica.valor)
		DatabaseSucursal.objects.get_or_create(name='SIC_Usuario_externo_Email',empresa_conexion=email.valor)
		DatabaseSucursal.objects.get_or_create(name='SIC_Usuario_externo_Password',empresa_conexion=password.valor)
		DatabaseSucursal.objects.get_or_create(name='SIC_Usuario_externo_Servidro_Correo',empresa_conexion=servidor_correo.valor)
		DatabaseSucursal.objects.get_or_create(name='SIC_Usuario_externo_Puerto',empresa_conexion=puerto.valor)

class UsuarioForm(forms.Form):
	usuario=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','place-holder':'Ingrese criterio de busqueda'}), required=False)
	anterior_contrasena=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
	nueva_contrasena=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)