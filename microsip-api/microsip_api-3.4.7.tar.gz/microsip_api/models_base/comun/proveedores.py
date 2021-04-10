#encoding:utf-8
from django.db import models

class ProveedorTipoBase(models.Model):
    id      = models.AutoField(primary_key=True, db_column='TIPO_PROV_ID')
    nombre  = models.CharField(max_length=30, db_column='NOMBRE')
   
    class Meta:
        db_table = u'tipos_prov'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

class ProveedorBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='PROVEEDOR_ID')
    nombre              = models.CharField(max_length=100, db_column='NOMBRE')
    cuenta_xpagar       = models.CharField(max_length=30, db_column='CUENTA_CXP', blank=True, null=True)
    cuenta_anticipos    = models.CharField(max_length=9, db_column='CUENTA_ANTICIPOS', blank=True, null=True)
    moneda              = models.ForeignKey('Moneda', db_column='MONEDA_ID',on_delete=models.CASCADE)
    tipo                = models.ForeignKey('ProveedorTipo', db_column='TIPO_PROV_ID',on_delete=models.CASCADE)
    rfc_curp            = models.CharField(max_length=18, db_column='RFC_CURP', blank=True, null=True)
    condicion_de_pago   = models.ForeignKey('CuentasXPagarCondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)
    #Direccion
    pais                = models.ForeignKey('Pais', db_column='PAIS_ID', blank=True, null=True,on_delete=models.CASCADE)
    estado              = models.ForeignKey('Estado', db_column='ESTADO_ID', blank=True, null=True,on_delete=models.CASCADE)
    ciudad              = models.ForeignKey('Ciudad', db_column='CIUDAD_ID',on_delete=models.CASCADE)
    
    TIPOS_OPERACION     = (('03', 'Prestacion de Servicios Profesionales'),('06', 'Arrendamiento de Inmuebles'),('85', 'Otros'),)
    actividad_principal = models.CharField(max_length=3, choices=TIPOS_OPERACION, db_column='ACTIVIDAD_PRINCIPAL', default='85')

    EXTRANJERO     = (('S', 'Si'),('N', 'No'),)
    es_extranjero = models.CharField(max_length=1, choices=EXTRANJERO, db_column='EXTRANJERO', default='N')

    class Meta:
        db_table = u'proveedores'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre

