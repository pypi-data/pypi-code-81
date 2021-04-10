#encoding:utf-8
from django.db import models
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class ImpuestoTipoBase(models.Model):
    id      = models.AutoField(primary_key=True, db_column='TIPO_IMPTO_ID')
    nombre  = models.CharField(max_length=30, db_column='NOMBRE')
    tipo    = models.CharField(max_length=30, db_column='TIPO')
    id_interno = models.CharField(max_length=1, db_column='ID_INTERNO')
    
    class Meta:
        db_table = u'tipos_impuestos'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)


class ImpuestoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='IMPUESTO_ID')
    nombre = models.CharField(max_length=30, db_column='NOMBRE')
    tipoImpuesto = models.ForeignKey('ImpuestoTipo', on_delete= models.SET_NULL, blank=True, null=True, db_column='TIPO_IMPTO_ID')
    if int(settings.MICROSIP_VERSION) >= 2013:
        TIPO_DE_CALCULO = (('P', 'Porcentaje'),)
        tipo_calculo = models.CharField(default='P', max_length=1, choices=TIPO_DE_CALCULO ,db_column='TIPO_CALC')
    TIPO_DE_IVA = (('1', 'General'),('2', 'Frontera'),('3', 'Tasa 0%'), ('4', 'Excento'),)
    tipo_iva = models.CharField(max_length=1, choices=TIPO_DE_IVA, blank=True, null=True, db_column='TIPO_IVA')
    
    porcentaje = models.DecimalField(default=0, blank=True, null=True, max_digits=9, decimal_places=6, db_column='PCTJE_IMPUESTO')
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='ES_PREDET')
        
    class Meta:
        db_table = u'impuestos'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)
        
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(ImpuestoBase, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
        
        super(ImpuestoBase, self).save(*args, **kwargs)

class ImpuestoArticuloBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='IMPUESTO_ART_ID')
    impuesto    = models.ForeignKey('Impuesto', db_column='IMPUESTO_ID',on_delete=models.CASCADE)
    articulo = models.ForeignKey('Articulo', on_delete= models.SET_NULL, blank=True, null=True, db_column='ARTICULO_ID')

    class Meta:
        db_table = u'impuestos_articulos'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.id)
        
    def save(self, *args, **kwargs):    
        using = kwargs.get('using', None)
        using = using or router.db_for_write(ImpuestoArticuloBase, instance=self)

        if self.id == None:
            self.id = next_id('ID_CATALOGOS', using)  
       
        super(ImpuestoArticuloBase, self).save(*args, **kwargs)

class VendedorBase(models.Model):
    id              = models.AutoField(primary_key=True, db_column='VENDEDOR_ID')
    nombre          = models.CharField(max_length=50, db_column='NOMBRE')

    class Meta:
        db_table = u'vendedores'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)