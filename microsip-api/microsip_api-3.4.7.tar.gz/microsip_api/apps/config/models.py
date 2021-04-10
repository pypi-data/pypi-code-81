from django.db import models
from ...models_base.config.config import *

# class DatabaseSucursal(models.Model):  
#     name = models.CharField(max_length=100)
#     empresa_conexion = models.CharField(max_length=200)
#     sucursal_conexion = models.CharField(max_length=200)
#     sucursal_conexion_name = models.CharField(max_length=200)
    
#     def __str__(self):  
#           return self.name    
          
#     class Meta:
#         app_label =u'auth'

# class Configuracion(ConfiguracionBase):
#     def save(self, *args, **kwargs):
#         if not self.id:
#             using = kwargs.get('using', None)
#             using = using or router.db_for_write(self.__class__, instance=self)
#             self.id = next_id('ID_CATALOGOS', using)

#         super(Configuracion, self).save(*args, **kwargs)

#     def get_value(self):
#         if self.valor == '':
#             return None
#         return self.valor

#     def __unicode__(self):
#         return u'%s' % self.nombre

class Usuario(UsuarioBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class UsuarioDerecho(UsuarioDerechoBase):
    def __unicode__(self):
        return u'%s - %s' % (self.usuario, self.clave_objeto)

class Empresa(EmpresaBase):
    def __unicode__(self):
        return u'%s' % self.nombre

class UsuarioEmpresa(UsuarioEmpresaBase):
    def __unicode__(self):
        return u'%s - %s' % (self.usuario, self.empresa)

    def natural_key(self):
        return (self.usuario, self.empresa)

class ReportBuilderFolder(ReportBuilderFolderBase):
    pass

class ReportBuilderItem(ReportBuilderItemBase):
    pass