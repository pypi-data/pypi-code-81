from django.db import models

# class ConfiguracionBase(models.Model):
#     id = models.AutoField(primary_key=True, db_column='ELEMENTO_ID')
#     nombre = models.CharField(max_length=100, db_column='NOMBRE')
#     tipo = models.CharField(max_length=1, db_column='TIPO')
#     padre = models.ForeignKey('self', related_name='padre_a', db_column='PADRE_ID' ,on_delete=models.CASCADE)
#     valor = models.CharField(default='', blank = True, null = True, max_length=100, db_column='VALOR')
    
#     class Meta:
#         db_table = u'registry'
#         abstract = True
#         managed= False
#         

class UsuarioBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='USUARIO_ID')
    nombre = models.CharField(max_length=100, db_column='NOMBRE')
    tipo = models.CharField(max_length=1, db_column='TIPO')
    acceso_empresas = models.CharField(max_length=1, db_column='ACCESO_EMPRESAS')
    usar_rol = models.CharField(default= 'N', max_length=1, db_column='USAR_ROL')
    # rol = models.ForeignKey( 'self', db_column = 'ROL_ID', related_name = 'rol_id', blank = True, null = True  ,on_delete=models.CASCADE)

    class Meta:
        db_table = u'usuarios'
        abstract = True
        managed= False
        

class UsuarioDerechoManager(models.Manager):
    def get_by_natural_key(self, usuario,  clave_objeto):
        return self.get(usuario=usuario, clave_objeto=clave_objeto)
        
class UsuarioDerechoBase(models.Model):
    objects = UsuarioDerechoManager()
    
    usuario = models.ForeignKey('Usuario', db_column='USUARIO_ID' ,on_delete=models.CASCADE)
    clave_objeto  = models.CharField(max_length=3, db_column='CLAVE_OBJETO')

    class Meta:
        db_table = u'derechos_usuarios'
        abstract = True
        managed= False
        
        unique_together = (('usuario', 'clave_objeto'),)

class EmpresaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='EMPRESA_ID')
    nombre = models.CharField(max_length=30, db_column='NOMBRE_CORTO')

    class Meta:
        db_table = u'empresas'
        abstract = True
        managed= False
        

class UsuarioEmpresaManager(models.Manager):
    def get_by_natural_key(self, usuario, empresa):
        return self.get(usuario=usuario, empresa=empresa)

class UsuarioEmpresaBase(models.Model):
    objects = UsuarioEmpresaManager()

    usuario = models.ForeignKey('Usuario', db_column='USUARIO_ID' ,on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', db_column='EMPRESA_ID' ,on_delete=models.CASCADE)

    class Meta:
        db_table = u'empresas_usuarios'
        abstract = True
        managed= False
        
        unique_together = (('usuario', 'empresa'),)


class ReportBuilderFolderBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='folder_id')
    name = models.CharField(max_length=60, db_column='name')
    parent = models.ForeignKey('self', related_name='parent_folder', db_column='parent_id' ,on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s'% self.name

    class Meta:
        db_table = u'rb_folder'
        abstract = True
        managed= False
        

class ReportBuilderItemBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='item_id')
    folder = models.ForeignKey('ReportBuilderFolder', db_column='folder_id' ,on_delete=models.CASCADE)
    name = models.CharField(max_length=60, db_column='name')
    item_size = models.IntegerField(blank=True, null=True, db_column='item_size')
    item_type = models.IntegerField(default=1, db_column='item_type')
    modified = models.FloatField(db_column='modified')
    deleted = models.FloatField(blank = True, null = True, db_column='deleted')
    template = models.TextField(db_column='template')
    
    class Meta:
        db_table = u'rb_item'
        abstract = True
        managed= False
        