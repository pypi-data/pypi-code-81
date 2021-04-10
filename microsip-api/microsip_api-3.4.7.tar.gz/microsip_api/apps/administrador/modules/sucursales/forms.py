#encoding:utf-8
from django import forms

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import fdb, os
from .models import *
from django.conf import settings

class DatabaseSucursalForm(forms.ModelForm):    
     class Meta:
        model = DatabaseSucursal
        exclude = ('empresa_conexion','sucursal_conexion_name',)

     def __init__(self,*args,**kwargs):
        bases_de_datos = settings.MICROSIP_DATABASES.keys()
        empresas = []
        for database_conexion in bases_de_datos:
            try:
                database_conexion = u'%s'%database_conexion
            except UnicodeDecodeError:
                pass
            else:
                conexion_split = database_conexion.split('-')
                conexion_id = conexion_split[0]
                empresa = '-'.join(conexion_split[1:])
                conexion = ConexionDB.objects.get(pk=int(conexion_id))
                database_conexion_name = "%s-%s"%(conexion.nombre, empresa)

                empresa_option = [database_conexion, database_conexion_name]
                empresas.append(empresa_option)
                    
        super(DatabaseSucursalForm,self).__init__(*args,**kwargs)
        self.fields['sucursal_conexion'] = forms.ChoiceField(choices= empresas)
