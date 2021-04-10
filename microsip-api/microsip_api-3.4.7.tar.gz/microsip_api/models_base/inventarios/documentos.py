#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from microsip_api.comun.sic_db import next_id

class InventariosDocumentoBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='DOCTO_IN_ID')
    folio               = models.CharField(max_length=50, db_column='FOLIO')
    almacen             = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    descripcion         = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    concepto            = models.ForeignKey('InventariosConcepto', db_column='CONCEPTO_IN_ID',on_delete=models.CASCADE)
    naturaleza_concepto = models.CharField(default='S', max_length=1, db_column='NATURALEZA_CONCEPTO')
    fecha               = models.DateField(db_column='FECHA') 
    cancelado           = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CANCELADO')
    aplicado            = models.CharField(default='S',blank=True, null=True, max_length=1, db_column='APLICADO')
    forma_emitida       = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='FORMA_EMITIDA')
    contabilizado       = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CONTABILIZADO')
    sistema_origen      = models.CharField(default='IN', max_length=2, db_column='SISTEMA_ORIGEN')
    usuario_creador     = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion  = models.DateTimeField(auto_now_add=True, db_column='FECHA_HORA_CREACION')
    usuario_ult_modif   = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')

    class Meta:
        db_table = u'doctos_in'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(InventariosDocumentoBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)            

        super(InventariosDocumentoBase, self).save(*args, **kwargs)

class InventariosDocumentoDetalleBase(models.Model):
    id              = models.AutoField(primary_key=True, db_column='DOCTO_IN_DET_ID')
    doctosIn        = models.ForeignKey('InventariosDocumento', db_column='DOCTO_IN_ID',on_delete=models.CASCADE)
    almacen         = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    concepto        = models.ForeignKey('InventariosConcepto', db_column='CONCEPTO_IN_ID',on_delete=models.CASCADE)
    claveArticulo   = models.CharField(blank=True, null=True, max_length=20, db_column='CLAVE_ARTICULO')
    articulo        = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    tipo_movto      = models.CharField(default='E', max_length=1, db_column='TIPO_MOVTO')
    unidades        = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='UNIDADES')
    costo_unitario  = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='COSTO_UNITARIO')
    costo_total     = models.DecimalField(default=0, blank=True, null=True, max_digits=15, decimal_places=2, db_column='COSTO_TOTAL')
    metodo_costeo   = models.CharField(default='C', max_length=1, db_column='METODO_COSTEO')
    cancelado       = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CANCELADO')
    aplicado        = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='APLICADO')
    costeo_pend     = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='COSTEO_PEND')
    pedimento_pend  = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='PEDIMENTO_PEND')
    rol             = models.CharField(default='N', max_length=1, db_column='ROL')
    fecha           = models.DateField(auto_now=True, blank=True, null=True, db_column='FECHA')

    class Meta:
        db_table = u'doctos_in_det'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(InventariosDocumentoDetalleBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(InventariosDocumentoDetalleBase, self).save(*args, **kwargs)

class InventariosDocumentoIFBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='DOCTO_INVFIS_ID')
    almacen             = models.ForeignKey('Almacen', db_column='ALMACEN_ID',on_delete=models.CASCADE)
    folio               = models.CharField(max_length=9, db_column='FOLIO')
    fecha               = models.DateField(db_column='FECHA') 
    cancelado           = models.CharField(default='N', blank=True, null=True, max_length=1, db_column='CANCELADO')
    aplicado            = models.CharField(default='N',blank=True, null=True, max_length=1, db_column='APLICADO')
    descripcion         = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    usuario_creador     = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion  = models.DateTimeField(auto_now_add=True, db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion= models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif   = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif   = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')

    class Meta:
        db_table = u'doctos_invfis'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.folio

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(InventariosDocumentoIFBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)

        super(InventariosDocumentoIFBase, self).save(*args, **kwargs)

class InventariosDocumentoIFDetalleBase(models.Model):
    id          = models.AutoField(primary_key=True, db_column='DOCTO_INVFIS_DET_ID')
    docto_invfis= models.ForeignKey('InventariosDocumentoIF', db_column='DOCTO_INVFIS_ID',on_delete=models.CASCADE)
    clave       = models.CharField(blank=True, null=True, max_length=20, db_column='CLAVE_ARTICULO')
    articulo    = models.ForeignKey('Articulo', db_column='ARTICULO_ID',on_delete=models.CASCADE)
    unidades    = models.DecimalField(default=0, blank=True, null=True, max_digits=18, decimal_places=5, db_column='UNIDADES')
    
    class Meta:
        db_table = u'doctos_invfis_det'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id