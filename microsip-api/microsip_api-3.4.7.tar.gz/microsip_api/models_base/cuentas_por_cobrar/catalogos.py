#encoding:utf-8
from django.db import models
from datetime import datetime

class CuentasXCobrarConceptoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CONCEPTO_CC_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    nombre_abrev = models.CharField(max_length=30, db_column='NOMBRE_ABREV')
    naturaleza = models.CharField(max_length=1, db_column='NATURALEZA')
    modalidad_facturacion = models.CharField(max_length=10, db_column='MODALIDAD_FACTURACION')
    folio_autom = models.CharField( default = 'N', max_length = 1, db_column = 'FOLIO_AUTOM' )
    sig_folio = models.CharField( max_length = 9, db_column = 'SIG_FOLIO' )
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    es_predefinod = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='ES_PREDEF')
    es_predeterminado = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='ES_PREDET')
    id_interno = models.CharField(max_length = 1, db_column = 'ID_INTERNO')
    crear_polizas = models.CharField(default='N', max_length=1, db_column='CREAR_POLIZAS')
    cuenta_contable = models.CharField(max_length=30, db_column='CUENTA_CONTABLE')
    clave_tipo_poliza = models.CharField(max_length=1, db_column='TIPO_POLIZA')
    descripcion_poliza = models.CharField(max_length=200, db_column='DESCRIPCION_POLIZA')
    tipo = models.CharField(max_length=1, db_column='TIPO')

    class Meta:
        db_table = u'conceptos_cc'
        abstract = True
        managed= False
        app_label='models_base'
        
    def __unicode__(self):
        return self.nombre_abrev