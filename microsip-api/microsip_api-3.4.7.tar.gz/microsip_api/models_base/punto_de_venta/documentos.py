#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class PuntoVentaDocumentoBase(models.Model):
    id                      = models.AutoField(primary_key=True, db_column='DOCTO_PV_ID')
    caja                    = models.ForeignKey('Caja', db_column='CAJA_ID',on_delete=models.CASCADE)
    cajero                  = models.ForeignKey('Cajero', db_column='CAJERO_ID',on_delete=models.CASCADE)
    cliente                 = models.ForeignKey('Cliente', db_column='CLIENTE_ID', related_name='cliente',on_delete=models.CASCADE)
    cliente_fac             = models.ForeignKey('Cliente', db_column='CLIENTE_FAC_ID', related_name='cliente_factura',on_delete=models.CASCADE)
    direccion_cliente       = models.ForeignKey('ClienteDireccion', db_column='DIR_CLI_ID',on_delete=models.CASCADE)
    almacen                 = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    moneda                  = models.ForeignKey('Moneda', db_column='MONEDA_ID',on_delete=models.CASCADE)
    vendedor                = models.ForeignKey('Vendedor', db_column='VENDEDOR_ID',on_delete=models.CASCADE)
    impuesto_sustituido     = models.ForeignKey('Impuesto', on_delete= models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_SUSTITUIDO_ID', related_name='impuesto_sustituido')
    impuesto_sustituto      = models.ForeignKey('Impuesto', on_delete= models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_SUSTITUTO_ID', related_name='impuesto_sustituto')

    tipo                    = models.CharField(max_length=1, db_column='TIPO_DOCTO')
    folio                   = models.CharField(max_length=9, db_column='FOLIO')
    fecha                   = models.DateField(db_column='FECHA')
    hora                    = models.TimeField(db_column='HORA')
    clave_cliente           = models.CharField(max_length=20, db_column='CLAVE_CLIENTE')
    clave_cliente_fac       = models.CharField(max_length=20, db_column='CLAVE_CLIENTE_FAC')
    impuesto_incluido       = models.CharField(default='S', max_length=1, db_column='IMPUESTO_INCLUIDO')
    tipo_cambio             = models.DecimalField(max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    tipo_descuento          = models.CharField(default='P',max_length=1, db_column='TIPO_DSCTO')
    porcentaje_descuento    = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='DSCTO_PCTJE')
    importe_descuento       = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='DSCTO_IMPORTE')
    estado                  = models.CharField(default='N', max_length=1, db_column='ESTATUS')
    aplicado                = models.CharField(default='N', max_length=1, db_column='APLICADO')
    importe_neto            = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_NETO')
    total_impuestos         = models.DecimalField(max_digits=15, decimal_places=2, db_column='TOTAL_IMPUESTOS')

    importe_donativo        = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_DONATIVO')
    total_fpgc              = models.DecimalField(max_digits=15, decimal_places=2, db_column='TOTAL_FPGC')
        
    ticket_emitido          = models.CharField(default='N', max_length=1, db_column='TICKET_EMITIDO')
    forma_emitida           = models.CharField(default='N', max_length=1, db_column='FORMA_EMITIDA')
    forma_global_emitida    = models.CharField(default='N', max_length=1, db_column='FORMA_GLOBAL_EMITIDA')
    contabilizado           = models.CharField(default='N', max_length=1, db_column='CONTABILIZADO')

    sistema_origen          = models.CharField(default='PV', max_length=2, db_column='SISTEMA_ORIGEN')
    cargar_sun              = models.CharField(default='S', max_length=1, db_column='CARGAR_SUN')
    persona                 = models.CharField(max_length=50, db_column='PERSONA')
    refer_reting            = models.CharField(blank=True, null=True, max_length=50, db_column='REFER_RETING')
    unidad_comprom          = models.CharField(default='N', max_length=1, db_column='UNID_COMPROM')    
    descripcion             = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    
    es_cfd                  = models.CharField(default='N', max_length=1, db_column='ES_CFD')
    modalidad_facturacion   = models.CharField(blank=True, null=True, max_length=10, db_column='MODALIDAD_FACTURACION')
    enviado                 = models.CharField(default='N', max_length=1, db_column='ENVIADO')
    email_envio             = models.EmailField(blank=True, null=True, db_column='EMAIL_ENVIO')
    fecha_envio             = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_ENVIO')

    #Factura global
    if int(settings.MICROSIP_VERSION) >= 2014:
        tipo_gen_fac = models.CharField(blank=True, null=True, max_length=1, db_column='TIPO_GEN_FAC')
        es_fac_global = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='ES_FAC_GLOBAL')
        fecha_ini_fac_global = models.DateField(blank=True, null=True, db_column='FECHA_INI_FAC_GLOBAL')
        fecha_fin_fac_global = models.DateField(blank=True, null=True, db_column='FECHA_FIN_FAC_GLOBAL')

    if int(settings.MICROSIP_VERSION) >= 2016:
        cfdi_certificado = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CFDI_CERTIFICADO')
    
    if int(settings.MICROSIP_VERSION) >= 2017:
        uso_cfdi = models.CharField(default='G01', blank=True, null=True, max_length=5, db_column='USO_CFDI')
        lugar_expedicion = models.IntegerField(db_column='LUGAR_EXPEDICION_ID')

    if int(settings.MICROSIP_VERSION) >= 2020:
        sucursal_id                = models.IntegerField(db_column='SUCURSAL_ID')

    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion      = models.DateTimeField(default=datetime.now().replace(hour=0), db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')

    usuario_cancelacion     = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CANCELACION')
    fechahora_cancelacion   = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_CANCELACION')
    usuario_aut_cancelacion = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CANCELACION')
    
    class Meta:
        db_table = u'doctos_pv'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        print("unicode",self.folio)
        return u'%s'% self.folio

    def _get_importe_total(self):
        print("total",self.folio)
        return self.importe_neto+self.total_impuestos
    importe_total = property(_get_importe_total)

    def save(self, *args, **kwargs):
        print("Save base")
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(PuntoVentaDocumentoBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(PuntoVentaDocumentoBase, self).save(*args, **kwargs)

class PuntoVentaDocumentoDetalleBase(models.Model):
    id                      = models.AutoField(primary_key=True, db_column='DOCTO_PV_DET_ID')
    documento_pv            = models.ForeignKey('PuntoVentaDocumento', db_column='DOCTO_PV_ID',on_delete=models.CASCADE)
    articulo                = models.ForeignKey('Articulo', on_delete= models.SET_NULL, blank=True, null=True, db_column='ARTICULO_ID')
    vendedor                = models.ForeignKey('Vendedor', blank=True, null=True, db_column='VENDEDOR_ID',on_delete=models.CASCADE)

    clave_articulo          = models.CharField(max_length=20, db_column='CLAVE_ARTICULO')
    unidades                = models.DecimalField(max_digits=18, decimal_places=5, db_column='UNIDADES')
    unidades_dev            = models.DecimalField(max_digits=18, decimal_places=5, db_column='UNIDADES_DEV')
    precio_unitario         = models.DecimalField(max_digits=18, decimal_places=6, db_column='PRECIO_UNITARIO')
    precio_unitario_impto   = models.DecimalField(max_digits=18, decimal_places=6, db_column='PRECIO_UNITARIO_IMPTO')
    porcentaje_descuento    = models.DecimalField(max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO')
    precio_total_neto       = models.DecimalField(max_digits=15, decimal_places=2, db_column='PRECIO_TOTAL_NETO')
    precio_modificado       = models.CharField(default='N', max_length=1, db_column='PRECIO_MODIFICADO')
    porcentaje_comis        = models.DecimalField(max_digits=9, decimal_places=6, db_column='PCTJE_COMIS')
    rol                     = models.CharField(max_length=1, db_column='ROL')
    notas                   = models.TextField(blank=True, null=True, db_column='NOTAS')
    es_tran_elect           = models.CharField(default='N', max_length=1, db_column='ES_TRAN_ELECT')
    estatus_tran_elect      = models.CharField(max_length=1,blank=True, null=True, db_column='ESTATUS_TRAN_ELECT')
    posicion                = models.IntegerField(db_column='POSICION')
    if int(settings.MICROSIP_VERSION) < 2017:
        fpgc_unitario           = models.DecimalField(max_digits=18, decimal_places=6, db_column='FPGC_UNITARIO')
    
    class Meta:
        db_table = u'doctos_pv_det'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s(%s)'% (self.id, self.documento_pv)
    
    def save(self, *args, **kwargs):
        
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(PuntoVentaDocumentoDetalleBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(PuntoVentaDocumentoDetalleBase, self).save(*args, **kwargs)

class PuntoVentaDocumentoLigaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_PV_LIGA_ID')
    docto_pv_fuente = models.ForeignKey('PuntoVentaDocumento', related_name='fuente', db_column='DOCTO_PV_FTE_ID',on_delete=models.CASCADE)
    docto_pv_destino = models.ForeignKey('PuntoVentaDocumento', related_name='destino', db_column='DOCTO_PV_DEST_ID',on_delete=models.CASCADE)
    
    class Meta:
        db_table = u'doctos_pv_ligas'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s'% self.id 
    
    def save(self, *args, **kwargs):
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(PuntoVentaDocumentoLigaBase, instance=self)
            self.id = next_id('ID_LIGAS_DOCTOS', using)

        super(PuntoVentaDocumentoLigaBase, self).save(*args, **kwargs)

class PuntoVentaDocumentoLigaDetalleManager(models.Manager):
    def get_by_natural_key(self, documento_liga,  detalle_fuente, detalle_destino):
        return self.get(documento_liga=documento_liga, detalle_fuente=detalle_fuente, detalle_destino=detalle_destino,)

class PuntoVentaDocumentoLigaDetalleBase(models.Model):    
    objects = PuntoVentaDocumentoLigaDetalleManager()
    documento_liga = models.ForeignKey('PuntoVentaDocumentoLiga', related_name='liga', db_column='DOCTO_PV_LIGA_ID',on_delete=models.CASCADE)
    detalle_fuente = models.ForeignKey('PuntoVentaDocumentoDetalle', related_name='fuente', db_column='DOCTO_PV_DET_FTE_ID',on_delete=models.CASCADE)
    detalle_destino = models.ForeignKey('PuntoVentaDocumentoDetalle', related_name='destino', db_column='DOCTO_PV_DET_DEST_ID',on_delete=models.CASCADE)

    class Meta:
        db_table = u'doctos_pv_ligas_det'
        unique_together = (('documento_liga', 'detalle_fuente','detalle_destino',),)
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s'% (self.documento_liga, self.detalle_fuente )

class PuntoVentaDocumentoDetalleTransferenciaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_PV_DET_ID')
    caja = models.ForeignKey('Caja', db_column='CAJA_ID',on_delete=models.CASCADE)
    cajero = models.ForeignKey('Cajero', db_column='CAJERO_ID',on_delete=models.CASCADE)
    params_text         = models.TextField(db_column='PARAMS_TEXT')
    clave_servicio      = models.CharField(max_length=10, db_column='CLAVE_SERVICIO')
    fecha               = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA')
    clave_receptor      = models.CharField(max_length=20, db_column='CLAVE_RECEPTOR')
    importe             = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE')
    costo               = models.DecimalField(max_digits=15, decimal_places=2, db_column='COSTO')
    autorizacion        = models.CharField(max_length=20, db_column='AUTORIZACION')
    fechahora_creacion  = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_CREACION')
    
    class Meta:
        db_table = u'doctos_pv_det_tran_elect'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s'% self.id 

class PuntoVentaCobroBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='DOCTO_PV_COBRO_ID')
    tipo                = models.CharField(max_length=1, db_column='TIPO')
    documento_pv        = models.ForeignKey('PuntoVentaDocumento', db_column='DOCTO_PV_ID',on_delete=models.CASCADE)
    forma_cobro         = models.ForeignKey('FormaCobro', db_column='FORMA_COBRO_ID',on_delete=models.CASCADE)
    importe             = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE')
    tipo_cambio         = models.DecimalField(max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    importe_mon_doc     = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_MON_DOC')
    
    class Meta:
        db_table = u'doctos_pv_cobros'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s'% self.id

class PuntoVentaCobroReferenciaBase(models.Model):
    referencia             = models.CharField(max_length=30, db_column='REFERENCIA')
    cobro_pv = models.ForeignKey('PuntoVentaCobro', db_column='DOCTO_PV_COBRO_ID',on_delete=models.CASCADE)
    forma_cobro_refer = models.ForeignKey('FormaCobroReferencia', db_column='FORMA_COBRO_REFER_ID',on_delete=models.CASCADE)
    
    class Meta:
        db_table = u'doctos_pv_cobros_refer'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s'% self.id 

class PuntoVentaDocumentoImpuestoManager(models.Manager):
    def get_by_natural_key(self, documento_pv,  impuesto):
        return self.get(documento_pv=documento_pv, impuesto=impuesto,)

class PuntoVentaDocumentoImpuestoBase(models.Model):
    objects = PuntoVentaDocumentoImpuestoManager()

    documento_pv        = models.ForeignKey('PuntoVentaDocumento', db_column='DOCTO_PV_ID',on_delete=models.CASCADE)
    impuesto            = models.ForeignKey('Impuesto', db_column='IMPUESTO_ID',on_delete=models.CASCADE)
    venta_neta          = models.DecimalField(max_digits=15, decimal_places=2, db_column='VENTA_NETA')
    otros_impuestos     = models.DecimalField(max_digits=15, decimal_places=2, db_column='OTROS_IMPUESTOS')
    porcentaje_impuestos= models.DecimalField(max_digits=9, decimal_places=6, db_column='PCTJE_IMPUESTO')
    importe_impuesto    = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_IMPUESTO')
    
    class Meta:
        db_table = u'impuestos_doctos_pv'
        unique_together = (('documento_pv', 'impuesto',),)
        abstract = True
        managed= False
        app_label='models_base'

class PuntoVentaDocumentoImpuestoGravadoBase(models.Model):
    impuesto_gravado    = models.DecimalField(max_digits=18, decimal_places=6, db_column='IMPUESTO_GRAVADO')
    listo               = models.CharField(max_length=1, default='N', db_column='LISTO')
    documento_pv        = models.ForeignKey('PuntoVentaDocumento', db_column='DOCTO_PV_ID',on_delete=models.CASCADE)
    articulo            = models.ForeignKey('Articulo', on_delete= models.SET_NULL, blank=True, null=True, db_column='ARTICULO_ID')
    impuesto            = models.ForeignKey('Impuesto', on_delete= models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_ID', related_name='impuesto')
    impuesto_grav       = models.ForeignKey('Impuesto', on_delete= models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_GARV_ID', related_name='impuesto_grav')

    class Meta:
        db_table = u'impuestos_grav_doctos_pv'
        abstract = True
        managed= False
        app_label='models_base'

class PuntoVentaArticuloDiscretoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DESGLOSE_DISCRETO_PV_ID')
    detalle = models.ForeignKey('PuntoVentaDocumentoDetalle', db_column='DOCTO_PV_DET_ID',on_delete=models.CASCADE)
    articulo_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID',on_delete=models.CASCADE)
    unidades = models.DecimalField(default=1, blank=True, null=True, max_digits=18, decimal_places=5, db_column='UNIDADES')
    
    class Meta:
        db_table = u'desglose_en_discretos_pv'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id