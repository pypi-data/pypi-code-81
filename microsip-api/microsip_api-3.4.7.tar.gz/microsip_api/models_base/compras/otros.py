#encoding:utf-8
from django.db import models
from django.db import router
from microsip_api.comun.sic_db import next_id

class AduanaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ADUANA_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    ciudad = models.ForeignKey('Ciudad', db_column='CIUDAD_ID' ,on_delete=models.CASCADE )
    gln = models.CharField(blank=True, null=True, max_length=20, db_column='GLN')
    es_predet = models.CharField(blank=True, null=True, max_length=20, db_column='ES_PREDET')

    usuario_creador = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion = models.DateTimeField(auto_now_add=True, db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now = True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')

    class Meta:
        db_table = u'aduanas'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

class PedimentoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PEDIMENTO_ID')
    clave = models.CharField(max_length=20, db_column='CLAVE')
    fecha = models.DateField(db_column='FECHA', blank=True, null=True)
    aduana_nombre = models.CharField(max_length=50, db_column='ADUANA')
    aduana = models.ForeignKey('Aduana', db_column='ADUANA_ID' ,on_delete=models.CASCADE )

    class Meta:
        db_table = u'pedimentos'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):
        
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(PedimentoBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)
           
        super(PedimentoBase, self).save(*args, **kwargs)

class DesglosePedimentoManager(models.Manager):
    def get_by_natural_key(self, inventario_documento_detalle,  pedimento):
        return self.get(inventario_documento_detalle= inventario_documento_detalle, pedimento= pedimento,)

class DesglosePedimentoBase(models.Model):
    objects = DesglosePedimentoManager()
    inventario_documento_detalle = models.ForeignKey('InventariosDocumentoDetalle', db_column='docto_in_det_id' ,on_delete=models.CASCADE )
    pedimento = models.ForeignKey('Pedimento', db_column='pedimento_id' ,on_delete=models.CASCADE )
    

    class Meta:
        db_table = u'desglose_en_pedimento'
        abstract = True
        managed= False
        app_label='models_base'
        unique_together = (('inventario_documento_detalle', 'pedimento',),)


class PedimentoCapaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='capa_pedimento_id')
    pedimento = models.ForeignKey('Pedimento', db_column='pedimento_id' ,on_delete=models.CASCADE )
    articulo = models.ForeignKey('Articulo', db_column='articulo_id' ,on_delete=models.CASCADE )
    articulo_discreto = models.ForeignKey('ArticuloDiscreto', blank=True, null=True, db_column='art_discreto_id' ,on_delete=models.CASCADE )
    almacen = models.ForeignKey('Almacen', db_column='almacen_id' ,on_delete=models.CASCADE )
    fecha = models.DateField(db_column='fecha')
    existencia = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='existencia')
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    capa_agotada = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='capa_agotada')

    class Meta:
        db_table = u'capas_pedimentos'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):
        
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(PedimentoCapaBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
           
        super(PedimentoCapaBase, self).save(*args, **kwargs)

# class PedimentoCapaUsoManager(models.Manager):
#     def get_by_natural_key(self, inventario_documento_detalle,  pedimento_capa):
#         return self.get(inventario_documento_detalle= inventario_documento_detalle, pedimento_capa= pedimento_capa,)

class PedimentoCapaUsoBase(models.Model):
    # objects = PedimentoCapaUsoManager()
    
    inventario_documento_detalle = models.ForeignKey('InventariosDocumentoDetalle', db_column='docto_in_det_id' ,on_delete=models.CASCADE )
    pedimento_capa = models.ForeignKey('PedimentoCapa', db_column='capa_pedimento_id' ,on_delete=models.CASCADE )
    unidades = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='unidades')
    TIPOS_USO = (('E', 'E'),)
    tipo_uso = models.CharField(max_length=1, choices=TIPOS_USO, db_column='tipo_uso')

    class Meta:
        db_table = u'USOS_CAPAS_PEDIMENTOS'
        abstract = True
        managed= False
        app_label='models_base'

