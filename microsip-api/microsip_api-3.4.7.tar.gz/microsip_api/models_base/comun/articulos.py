#encoding:utf-8
from django.db import models, connections, router
from microsip_api.comun.sic_db import next_id
from datetime import datetime
from django.conf import settings

class GrupoLineasBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='GRUPO_LINEA_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    cuenta_ventas= models.CharField(max_length=30, db_column='CUENTA_VENTAS')
    
    class Meta:
        db_table = u'grupos_lineas'
        abstract  = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre
        
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(GrupoLineasBase, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(GrupoLineasBase, self).save(*args, **kwargs)

class LineaArticulosBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='LINEA_ARTICULO_ID')
    grupo = models.ForeignKey('GrupoLineas', blank = True, null = True, db_column='GRUPO_LINEA_ID',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    cuenta_ventas = models.CharField(max_length=30, db_column='CUENTA_VENTAS')

    class Meta:
        db_table = u'lineas_articulos'
        abstract  = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre
        
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(LineaArticulosBase, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  

        super(LineaArticulosBase, self).save(*args, **kwargs)


class ArticuloBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ARTICULO_ID')
    linea = models.ForeignKey('LineaArticulos', blank=True, null=True, db_column='LINEA_ARTICULO_ID',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, db_column='NOMBRE')
    es_juego = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='es_juego')
    SI_O_NO = (('S', 'Si'), ('N', 'No'),)
    es_almacenable = models.CharField(default='S', max_length=1, choices=SI_O_NO, db_column='ES_ALMACENABLE')
    es_importado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='es_importado')
    es_peso_variable = models.CharField(default='N', blank=True, null=True, max_length=1, choices=SI_O_NO, db_column='es_peso_variable')
    estatus = models.CharField(default='A', max_length=1, db_column='ESTATUS')
    seguimiento = models.CharField(default='N', max_length=1, db_column='SEGUIMIENTO')
    cuenta_ventas = models.CharField(max_length=30, blank=True, null=True, db_column='CUENTA_VENTAS')
    nota_ventas = models.TextField(db_column='NOTAS_VENTAS', blank=True, null=True)
    unidad_venta = models.CharField(default='PIEZA', max_length=20, blank=True, null=True, db_column='UNIDAD_VENTA')
    unidad_compra = models.CharField(default='PIEZA', max_length=20, blank=True, null=True, db_column='UNIDAD_COMPRA')
    print( settings.MICROSIP_VERSION)
    if settings.MICROSIP_VERSION < '2018':
        costo_ultima_compra = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=6, db_column='COSTO_ULTIMA_COMPRA')
        fecha_ultima_compra = models.DateField(db_column='FECHA_ULTIMA_COMPRA', blank=True, null=True)

    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')

    class Meta:
        db_table = u'articulos'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__(self):
        return u'%s (%s)' % (self.nombre, self.unidad_venta)

    def get_descuento_total(self, *args, **kwargs):
        using = kwargs.get('using', None)
        cliente_id = kwargs.get('cliente_id', None)
        unidades = kwargs.get('unidades', None)

        using = using or router.db_for_write(ArticuloBase, instance=self)
        c = connections[using].cursor()
        c.execute('''execute procedure get_dscto_art(%s,%s,current_date,current_timestamp,%s)''' % (cliente_id, self.id, unidades))
        descuento = c.fetchall()[0][0]

        c.close()

        return descuento

    def get_existencia(self, *args, **kwargs):
        using = kwargs.get('using', None)
        almacen_nombre = kwargs.get('almacen_nombre', None)
        using = using or router.db_for_write(ArticuloBase, instance=self)
        c = connections[using].cursor()
        fecha_inicio = datetime.now().strftime("01/01/%Y")
        fecha_fin = datetime.now().strftime("12/31/%Y")
        c.execute('''select INV_FIN_UNID as existencia from orsp_in_aux_art( %s, '%s', '%s','%s','S','N')''' % (self.id, almacen_nombre, fecha_inicio, fecha_fin))
        exsistencia = c.fetchall()[0][0]
        c.close()
        return exsistencia

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(ArticuloBase, instance=self)

        if self.id is None:
            self.id = next_id('ID_CATALOGOS', using)

        super(ArticuloBase, self).save(*args, **kwargs)


class ArticuloClaveRolBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ROL_CLAVE_ART_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    es_ppal = models.CharField(default='N', max_length=1, db_column='ES_PPAL')

    class Meta:
        db_table = u'roles_claves_articulos'
        abstract  = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

class ArticuloClaveBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CLAVE_ARTICULO_ID')
    clave = models.CharField(max_length=20, db_column='CLAVE_ARTICULO')
    articulo = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    rol = models.ForeignKey('ArticuloClaveRol', db_column='ROL_CLAVE_ART_ID',on_delete=models.CASCADE)
    
    class Meta:
        db_table = u'claves_articulos'
        abstract  = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.clave

    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(ArticuloClaveBase, instance=self)
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(ArticuloClaveBase, self).save(*args, **kwargs)

class ArticuloPrecioBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PRECIO_ARTICULO_ID')
    articulo = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    precio_empresa = models.ForeignKey('PrecioEmpresa', db_column='PRECIO_EMPRESA_ID',on_delete=models.CASCADE)
    moneda =  models.ForeignKey('Moneda', db_column='MONEDA_ID',on_delete=models.CASCADE)
    precio = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=6, db_column='PRECIO')
    margen = models.DecimalField(default=0, blank=True, null=True, max_digits=9, decimal_places=6, db_column='MARGEN')
    class Meta:
        db_table = u'precios_articulos'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(ArticuloPrecioBase, instance=self)
        if self.id == None or self.id == -1:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(ArticuloPrecioBase, self).save(*args, **kwargs)

class AlmacenBase(models.Model):
    ALMACEN_ID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    nombre_abrev = models.CharField(max_length=50, db_column='NOMBRE_ABREV')
    es_predet = models.CharField(blank=True, null=True, max_length=20, db_column='ES_PREDET')

    class Meta:
        db_table = u'almacenes'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return self.nombre

class PrecioEmpresaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PRECIO_EMPRESA_ID')
    nombre = models.CharField(default='N', max_length=30, db_column='NOMBRE')
    posicion = models.CharField(max_length=2, db_column='POSICION')
        
    class Meta:
        db_table = u'precios_empresa'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(PrecioEmpresaBase, instance=self)
        
        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  

        super(PrecioEmpresaBase, self).save(*args, **kwargs)

class ArticuloDiscretoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ART_DISCRETO_ID')
    clave = models.CharField(max_length=20, db_column='CLAVE')
    articulo = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, db_column='TIPO')
    fecha = models.DateField(db_column='FECHA', blank=True, null=True)
    
    class Meta:
        db_table = u'articulos_discretos'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.clave

class ArticuloDiscretoExistenciaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='EXIS_DISCRETO_ID')
    articulo_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID',on_delete=models.CASCADE)
    almacen = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    existencia = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=5, db_column='EXISTENCIA')
    
    class Meta:
        db_table = u'exis_discretos'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

class ArticuloNivelBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='NIVEL_ART_ID')
    articulo = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    almacen = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    localizacion = models.CharField(max_length=15)
    maximo = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=5, db_column='INVENTARIO_MAXIMO')
    reorden = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=5, db_column='PUNTO_REORDEN')
    minimo = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=5, db_column='INVENTARIO_MINIMO')

    class Meta:
        db_table = u'NIVELES_ARTICULOS'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s-%s' % (self.id, self.localizacion)

class ClasificadoresBase(models.Model):
    clasificador_id=models.AutoField(primary_key=True, db_column='CLASIFICADOR_ID')
    tipo_objeto = models.CharField(max_length=1, db_column="TIPO_OBJETO")
    nombre = models.CharField(max_length=50, db_column="NOMBRE")
    nombre_abrev = models.CharField(max_length=30, db_column="NOMBRE_ABREV")
    descripcion = models.TextField(db_column='DESCRIPCION', null=True)
    usuario_creador = models.CharField(max_length=31, db_column="USUARIO_CREADOR", null=True)
    fecha_hora_creacion = models.DateTimeField(db_column='FECHA_HORA_CREACION', blank=True, null=True)
    usuario_aut_creacion = models.CharField(max_length=31, db_column="USUARIO_AUT_CREACION", null=True)
    usuario_ult_modif = models.CharField(max_length=31, db_column="USUARIO_ULT_MODIF", null=True)
    fecha_hora_ult_modif = models.DateTimeField(db_column='FECHA_HORA_ULT_MODIF', blank=True, null=True)
    usuario_aut_modif = models.CharField(max_length=31, db_column="USUARIO_AUT_MODIF", null=True)

    class Meta:
        db_table = u'CLASIFICADORES_CAT'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % (self.nombre)

class ClasificadoresValoresBase(models.Model):
    valor_clasif_id = models.AutoField(primary_key=True, db_column='VALOR_CLASIF_ID')
    clasificador = models.ForeignKey('Clasificadores', db_column='CLASIFICADOR_ID',on_delete=models.CASCADE)
    valor = models.CharField(max_length=50   , db_column="VALOR")
    posicion = models.SmallIntegerField(db_column="POSICION")
    
    class Meta:
        db_table = u'CLASIFICADORES_CAT_VALORES'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % (self.valor)
    
class ElementosClasificadoresBase(models.Model):
    elemento_id = models.IntegerField(primary_key=True,db_column="ELEMENTO_ID")
    valor_clasificador = models.ForeignKey('ClasificadoresValores', db_column='VALOR_CLASIF_ID',on_delete=models.CASCADE)

    
    class Meta:
        db_table = u'ELEMENTOS_CAT_CLASIF'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % (self.valor_clasificador)
        
    




        

    
    
    
    
    


