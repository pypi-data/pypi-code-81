#encoding:utf-8
from django.db import models
from django.db import router
from datetime import datetime

from microsip_api.comun.comun_functions import split_letranumero
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class CuentasXCobrarDocumentoBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    MODALIDADES_FACTURACION = (('PREIMP', 'PREIMP'),)
    id = models.AutoField(primary_key=True, db_column='DOCTO_CC_ID')
    concepto = models.ForeignKey('CuentasXCobrarConcepto', db_column='CONCEPTO_CC_ID',on_delete=models.CASCADE)
    folio = models.CharField(max_length=9, db_column='FOLIO')
    naturaleza_concepto = models.CharField(max_length=1, db_column='NATURALEZA_CONCEPTO')
    fecha = models.DateField(db_column='FECHA')
    cliente = models.ForeignKey('Cliente', db_column='CLIENTE_ID',on_delete=models.CASCADE)
    cliente_clave = models.CharField(max_length=20, blank=True, null=True, db_column='CLAVE_CLIENTE')
    
    if int(settings.MICROSIP_VERSION) >= 2013:
        cobro_importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='IMPORTE_COBRO')
        estatus_anterior = models.CharField(default='N', max_length=1, db_column='ESTATUS_ANT')
        integ_ba = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='INTEG_BA')
        contabilizado_ba = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CONTABILIZADO_BA')
        referencia_movimiento_bancario = models.CharField(max_length=9, blank=True, null=True, db_column='REFER_MOVTO_BANCARIO')
    
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    cancelado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CANCELADO')
    aplicado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='APLICADO')
    descripcion = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    cuenta_concepto = models.CharField(max_length=30, blank=True, null=True, db_column='CUENTA_CONCEPTO')
    # cobrador                      = models.ForeignKey('C', db_column='COBRADOR_ID',on_delete=models.CASCADE)
    forma_emitida = models.CharField(default='N', max_length=1, blank=True, null=True, choices=SI_O_NO ,db_column='FORMA_EMITIDA')
    contabilizado = models.CharField(default='N', blank=True, null=True, max_length=1, choices=SI_O_NO, db_column='CONTABILIZADO')
    contabilizado_gyp = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CONTABILIZADO_GYP')
    
    condicion_pago = models.ForeignKey('CondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)
    descuentoxprontopago_fecha = models.DateField(blank=True, null=True, db_column='FECHA_DSCTO_PPAG')    
    descuentoxprontopago_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO_PPAG')
    
    factura_mostrador_folio = models.CharField(max_length=9, blank=True, null=True, db_column='FACTURA_MOSTRADOR')
    sistema_origen = models.CharField(default='CC', max_length=2, db_column='SISTEMA_ORIGEN')
    estatus = models.CharField(default='N', max_length=1, db_column='ESTATUS')
    fecha_aplicacion = models.DateField(blank=True, null=True, db_column='FECHA_APLICACION')

    es_cfd = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='ES_CFD')
    modalidad_facturacion = models.CharField(default='PREIMP', max_length=10, choices=MODALIDADES_FACTURACION, db_column='MODALIDAD_FACTURACION')
    enviado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ENVIADO')
    envio_fechahora = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_ENVIO')
    envio_email = models.EmailField(blank=True, null=True, db_column='EMAIL_ENVIO')
    cfd_certificado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CFDI_CERTIFICADO')
    
    # cuenta_banncaria = models.CharField(max_length=30, db_column='CUENTA_BANCOS')
    creacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')                             
    creacion_fechahora = models.DateTimeField(default=datetime.now().replace(hour=0), db_column='FECHA_HORA_CREACION')   
    creacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')        
    modificacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')           
    modificacion_fechahora = models.DateTimeField(auto_now = True, db_column='FECHA_HORA_ULT_MODIF')                         
    modificacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')           
    cancelacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CANCELACION')         
    cancelacion_fechahora = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_CANCELACION')                 
    cancelacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CANCELACION')

    class Meta:
        db_table = u'doctos_cc'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

    def next_folio( self, using=None):
        """ Generar un folio nuevo del concepto del documento e incrementa el consecutivo de folio """
        concepto = self.concepto    
        folio = concepto.sig_folio

        prefijo, consecutivo = split_letranumero(concepto.sig_folio)
        consecutivo +=1
        concepto.sig_folio = '%s%s'% (prefijo,("%09d" % consecutivo)[len(prefijo):])
        concepto.save( update_fields=('sig_folio',) )

        return folio

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(CuentasXCobrarDocumentoBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
            self.naturaleza_concepto = self.concepto.naturaleza

            if self.concepto.sig_folio and not self.folio:
                self.folio = self.next_folio(using=using)
        super(CuentasXCobrarDocumentoBase, self).save(*args, **kwargs)

class CuentasXCobrarDocumentoImportesBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    TIPOS_IMPORTE = (('C', 'C'),('R', 'R'),)
    id = models.AutoField(primary_key=True, db_column='IMPTE_DOCTO_CC_ID')
    docto_cc = models.ForeignKey('CuentasXCobrarDocumento', db_column='DOCTO_CC_ID',on_delete=models.CASCADE)
    if int(settings.MICROSIP_VERSION) >= 2013:
        fecha = models.DateField(db_column='FECHA')
    cancelado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CANCELADO')
    aplicado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='APLICADO')
    estatus = models.CharField(default='N', max_length=1, db_column='ESTATUS')

    doocumento_acr = models.ForeignKey('CuentasXCobrarDocumento', blank=True, null=True, related_name='doocumento_acr', db_column='DOCTO_CC_ACR_ID',on_delete=models.CASCADE)
    tipo_importe = models.CharField(default='C', choices=TIPOS_IMPORTE, blank=True, null=True, max_length=1, db_column='TIPO_IMPTE')
    importe = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE')
    total_impuestos = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPUESTO')
    iva_retenido = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='IVA_RETENIDO')
    isr_retenido = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='ISR_RETENIDO')
    descuentoxprontopago = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='DSCTO_PPAG')
    comisiones_porcentaje = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='PCTJE_COMIS_COB')
    
    class Meta:
        db_table = u'importes_doctos_cc'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(CuentasXCobrarDocumentoImportesBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
            
        super(CuentasXCobrarDocumentoImportesBase, self).save(*args, **kwargs)


class CuentasXCobrarDocumentoImportesImpuestoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='impte_docto_cc_impto_id')
    importe = models.ForeignKey('CuentasXCobrarDocumentoImportes', db_column='impte_docto_cc_id',on_delete=models.CASCADE)
    importe_venta_neta = models.DecimalField(max_digits=15, decimal_places=2, db_column='importe')
    impuesto = models.ForeignKey('Impuesto', db_column='impuesto_id',on_delete=models.CASCADE)
    impuesto_importe = models.DecimalField(max_digits=15, decimal_places=2, db_column='impuesto')
    impuesto_porcentaje = models.DecimalField(max_digits=9, decimal_places=6, db_column='pctje_impuesto')
    
    class Meta:
        db_table = u'importes_doctos_cc_imptos'
        abstract = True
        managed= False
        app_label='models_base'
        
class CuentasXCobrarDocumentoCargoVencimientoBase(models.Model):
    documento = models.ForeignKey('CuentasXCobrarDocumento', unique_for_date='fecha', db_column='docto_cc_id',on_delete=models.CASCADE)
    fecha = models.DateField(db_column='fecha_vencimiento') 
    porcentaje_de_venta = models.PositiveSmallIntegerField( db_column='pctje_ven')

    class Meta:
        db_table = u'vencimientos_cargos_cc'
        abstract = True
        managed= False
        app_label='models_base'

class CuentasXCobrarDocumentoCargoLibresBase(models.Model):
    id            = models.AutoField(primary_key=True, db_column='DOCTO_CC_ID')
    
    class Meta:
        db_table = u'libres_cargos_cc'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

class CuentasXCobrarDocumentoCreditoLibresBase(models.Model):
    id            = models.AutoField(primary_key=True, db_column='DOCTO_CC_ID')
    
    class Meta:
        db_table = u'libres_creditos_cc'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id