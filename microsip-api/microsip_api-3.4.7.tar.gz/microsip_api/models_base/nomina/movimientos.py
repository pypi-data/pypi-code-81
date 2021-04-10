#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from django.conf import settings

class NominaPrestamoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='prestamo_emp_id')

    #General
    empleado = models.ForeignKey('NominaEmpleado', db_column='empleado_id',on_delete=models.CASCADE)
    concepto = models.ForeignKey('NominaConcepto', db_column='concepto_no_id',on_delete=models.CASCADE)
    fecha = models.DateField(db_column='fecha')
    importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='importe')
    cuota = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='cuota')
    fecha_ini_ret = models.DateField(db_column='fecha_ini_ret')
    descripcion = models.CharField(blank=True, null=True, max_length=200, db_column='descripcion')
    cuenta_contable = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_contable')
    estatus = models.CharField(max_length=1, db_column='estatus')
    fecha_fin = models.DateField(blank=True, null=True, db_column='FECHA_FIN')
    usuario_creador = models.CharField(max_length=31, db_column='usuario_creador')
    fechahora_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')
    usuario_cancelacion = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_cancelacion')
    fechahora_cancelacion = models.DateTimeField(blank=True, null=True, db_column='fecha_hora_cancelacion')
    usuario_aut_cancelacion = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_cancelacion')

    class Meta:
        db_table = u'prestamos_emp'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.id

