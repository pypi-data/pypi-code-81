#encoding:utf-8
from django.db import models
from django.db import router
from microsip_api.comun.sic_db import next_id


class ClaveGeneralManager(models.Manager):
    def get_by_natural_key(self, tabla_nombre,  elemento_id):
        return self.get(tabla_nombre=tabla_nombre, elemento_id=elemento_id,)


class ClaveGeneralBase(models.Model):
    objects = ClaveGeneralManager()
    tabla_nombre = models.CharField(max_length=31, db_column='nombre_tabla')
    elemento_id = models.IntegerField(db_column='elem_id')
    clave = models.CharField(max_length=20, db_column='clave')

    class Meta:
        db_table = u'claves_cat_sec'
        abstract = True
        managed= False
        app_label='models_base'
        unique_together = (('tabla_nombre', 'elemento_id',),)


class PaisBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PAIS_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    nombre_abreviado = models.CharField(max_length=10, db_column='NOMBRE_ABREV')

    SI_O_NO = (('S', 'Si'), ('N', 'No'),)
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ES_PREDET')

    class Meta:
        db_table = u'paises'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(PaisBase, instance=self)

        if self.id is None:
            self.id = next_id('ID_CATALOGOS', using)

        super(PaisBase, self).save(*args, **kwargs)


class EstadoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ESTADO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    pais = models.ForeignKey('Pais', blank=True, null=True, db_column='PAIS_ID',on_delete=models.CASCADE)
    nombre_abreviado = models.CharField(max_length=10, db_column='NOMBRE_ABREV')

    SI_O_NO = (('S', 'Si'), ('N', 'No'),)
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ES_PREDET')

    class Meta:
        db_table = u'estados'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s, %s' % (self.nombre, self.pais)

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(EstadoBase, instance=self)

        if self.id is None:
            self.id = next_id('ID_CATALOGOS', using)
        super(EstadoBase, self).save(*args, **kwargs)


class CiudadBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CIUDAD_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    estado = models.ForeignKey('Estado', db_column='ESTADO_ID',on_delete=models.CASCADE)
    SI_O_NO = (('S', 'Si'), ('N', 'No'),)
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ES_PREDET')

    class Meta:
        db_table = u'ciudades'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s, %s' % (self.nombre, self.estado)

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(CiudadBase, instance=self)

        if self.id is None:
            self.id = next_id('ID_CATALOGOS', using)

        super(CiudadBase, self).save(*args, **kwargs)


class MonedaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='moneda_id')
    es_moneda_local = models.CharField(default='N', max_length=1, db_column='es_moneda_local')
    nombre = models.CharField(max_length=30, db_column='nombre')
    simbolo = models.CharField(max_length=10, db_column='simbolo')
    es_predet = models.CharField(blank=True, null=True, max_length=20, db_column='es_predet')

    class Meta:
        db_table = u'monedas'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        using = using or router.db_for_write(MonedaBase, instance=self)

        if self.id is None:
            self.id = next_id('ID_CATALOGOS', using)

        super(MonedaBase, self).save(*args, **kwargs)


class TipoCambioBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='HISTORIA_CAMB_ID')
    moneda = models.ForeignKey('Moneda', db_column='MONEDA_ID',on_delete=models.CASCADE)
    fecha = models.DateField(db_column='FECHA')
    tipo_cambio = models.DecimalField(default=1, max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    tipo_cambio_cobros = models.DecimalField(default=1, max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO_COBROS')

    usuario_creador = models.CharField(max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion = models.DateTimeField(auto_now_add=True, db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')

    class Meta:
        db_table = u'historia_cambiaria'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id


class ViaEmbarqueBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='VIA_EMBARQUE_ID')
    nombre = models.CharField(max_length=20, db_column='NOMBRE')
    es_predet = models.CharField(default='N', max_length=1, db_column='ES_PREDET')

    usuario_creador = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')

    class Meta:
        db_table = u'vias_embarque'
        abstract = True
        managed= False
        app_label='models_base'


class FolioVentaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='FOLIO_VENTAS_ID')
    tipo_doc = models.CharField(max_length=1, db_column='TIPO_DOCTO')
    serie = models.CharField(max_length=3, db_column='SERIE')
    consecutivo = models.IntegerField(db_column='CONSECUTIVO')
    modalidad_facturacion = models.CharField(max_length=10, db_column='MODALIDAD_FACTURACION')
    # punto_reorden = models.IntegerField(db_column='PUNTO_REORDEN_FOLIOS')
    # dias_reorden = models.IntegerField(db_column='DIAS_REORDEN_FOLIOS')

    class Meta:
        db_table = u'folios_ventas'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id


class FolioCompraBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='FOLIO_COMPRAS_ID')
    tipo_doc = models.CharField(max_length=1, db_column='TIPO_DOCTO')
    serie = models.CharField(max_length=3, db_column='SERIE')
    consecutivo = models.IntegerField(db_column='CONSECUTIVO')

    class Meta:
        db_table = u'folios_compras'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id


class AtributoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ATRIBUTO_ID')
    nombre = models.CharField(max_length=31, db_column='NOMBRE')
    nombre_columna = models.CharField(max_length=31, db_column='NOMBRE_COLUMNA')
    clave_objeto = models.CharField(max_length=20, db_column='CLAVE_OBJETO')
    posicion = models.IntegerField(db_column='POSICION')
    tipo = models.CharField(max_length=1, db_column='TIPO')
    longitud = models.IntegerField(db_column='LONGITUD')
    escala = models.IntegerField(db_column='ESCALA')
    valor_minimo = models.DecimalField(max_digits=18, decimal_places=5, db_column='VALOR_MINIMO')
    valor_maximo = models.DecimalField(max_digits=18, decimal_places=5, db_column='VALOR_MAXIMO')
    valor_default_numerico = models.DecimalField(max_digits=18, decimal_places=5, db_column='VALOR_DEFAULT_NUMERICO')
    valor_default_caracter = models.CharField(max_length=100,db_column='VALOR_DEFAULT_CARACTER')
    descripcion = models.TextField(db_column='DESCRIPCION')

    class Meta:
        db_table = u'ATRIBUTOS'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

class AtributoListaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='LISTA_ATRIB_ID')
    atributo = models.ForeignKey('Atributo', db_column='ATRIBUTO_ID',on_delete=models.CASCADE)
    valor = models.CharField(max_length=50, db_column='VALOR_DESPLEGADO')
    posicion = models.IntegerField(db_column='POSICION')

    class Meta:
        db_table = u'LISTAS_ATRIBUTOS'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.valor