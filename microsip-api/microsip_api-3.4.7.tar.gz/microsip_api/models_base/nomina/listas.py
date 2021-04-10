#encoding:utf-8
from django.db import models

class NominaTablaTipoBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    id = models.AutoField(primary_key=True, db_column='TIPO_TABLA_NO_ID')
    nombre = models.CharField(max_length=50, db_column='nombre')
    id_interno = models.CharField(max_length=1, blank=True, null=True, db_column='id_interno')
    preg_ano = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='preg_ano')
    varias_por_ano = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='varias_por_ano')
    escalable = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='escalable')

    class Meta:
        db_table = u'tipos_tablas_no'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.nombre

class NominaTablaBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    id = models.AutoField(primary_key=True, db_column='tabla_no_id')
    nombre = models.CharField(max_length=50, db_column='nombre')
    tipo = models.ForeignKey('NominaTablaTipo', db_column='tipo_tabla_no_id',on_delete=models.CASCADE)
    anio = models.IntegerField(db_column='ano')
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='es_predet')
    #otros
    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion      = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')
    
    class Meta:
        db_table = u'tablas_no'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.nombre

