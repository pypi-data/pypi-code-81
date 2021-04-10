#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from microsip_api.comun.sic_db import next_id

class CuentasXPagarDocumentoBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='DOCTO_CP_ID')
    concepto            = models.ForeignKey('CuentasXPagarConcepto', db_column='CONCEPTO_CP_ID',on_delete=models.CASCADE)
    folio               = models.CharField(max_length=9, db_column='FOLIO')
    naturaleza_concepto = models.CharField(max_length=1, db_column='NATURALEZA_CONCEPTO')
    fecha               = models.DateField(db_column='FECHA') 
    proveedor           = models.ForeignKey('Proveedor', db_column='PROVEEDOR_ID',on_delete=models.CASCADE)
    cancelado           = models.CharField(default='N', max_length=1, db_column='CANCELADO')
    aplicado            = models.CharField(default='S', max_length=1, db_column='APLICADO')
    descripcion         = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    contabilizado       = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CONTABILIZADO')
    tipo_cambio         = models.DecimalField(max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    condicion_pago      = models.ForeignKey('CuentasXPagarCondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)

    class Meta:
        db_table = u'doctos_cp'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

class CuentasXPagarDocumentoImportesBase(models.Model):
    id              = models.AutoField(primary_key=True, db_column='IMPTE_DOCTO_CP_ID')
    docto_cp        = models.ForeignKey('CuentasXPagarDocumento', db_column='DOCTO_CP_ID',on_delete=models.CASCADE)
    importe         = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE')
    total_impuestos = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPUESTO')
    iva_retenido    = models.DecimalField(max_digits=15, decimal_places=2, db_column='IVA_RETENIDO')
    isr_retenido    = models.DecimalField(max_digits=15, decimal_places=2, db_column='ISR_RETENIDO')
    dscto_ppag      = models.DecimalField(max_digits=15, decimal_places=2, db_column='DSCTO_PPAG')
    cancelado       = models.CharField(default='N', max_length=1, db_column='CANCELADO')
    
    class Meta:
        db_table = u'importes_doctos_cp'
        abstract = True
        managed= False
        app_label='models_base'

class CuentasXPagarDocumentoImportesImpuestoBase(models.Model):
    id               = models.AutoField(primary_key=True, db_column='IMPTE_DOCTO_CP_IMPTO_ID')
    documento_importes = models.ForeignKey('CuentasXPagarDocumentoImportes', db_column='IMPTE_DOCTO_CP_ID',on_delete=models.CASCADE)
    impuesto         = models.ForeignKey('Impuesto', db_column='IMPUESTO_ID',on_delete=models.CASCADE)
    importe          = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE')
    porcentaje       = models.DecimalField(max_digits=9, decimal_places=6, db_column='PCTJE_IMPUESTO')    
    impuesto         = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPUESTO')
    
    class Meta:
        db_table = u'importes_doctos_cp_imptos'
        abstract = True
        managed= False
        app_label='models_base'

class CuentasXPagarDocumentoCargoLibresBase(models.Model):
    id            = models.AutoField(primary_key=True, db_column='DOCTO_CP_ID')
    
    class Meta:
        db_table = u'libres_cargos_cp'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id