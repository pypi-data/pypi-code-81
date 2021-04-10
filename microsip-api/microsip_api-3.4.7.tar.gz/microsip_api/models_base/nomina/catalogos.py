#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class NominaEmpleadoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='empleado_id')
    #General
    nombre_completo = models.CharField(max_length=50, db_column='nombre_completo')
    numero = models.IntegerField(db_column='numero')
    
    class Meta:
        db_table = u'empleados'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.nombre_completo

class NominaFrecuenciaPagoBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    PAGO_TIPOS = (('D', 'Por día'), ('H', 'Por hora'),)
    PROCESO_TIPOS = (('A', 'Automático'), ('M', 'Manual'),)
    ISR_TARIFAS = (('M', 'ISR mensual'),)

    id = models.AutoField(primary_key=True, db_column='frepag_id')
    #General
    nombre = models.CharField(max_length=50, db_column='nombre')
    periodo_dias = models.DecimalField(max_digits=5, decimal_places=2, db_column='dias_periodo')
    a_cotizar_dias = models.DecimalField(max_digits=7, decimal_places=4, db_column='dias_a_cot')
    pago_tipo = models.CharField(max_length=1, choices=PAGO_TIPOS, db_column='tipo_pago')
    periodo_horas = models.DecimalField(max_digits=5, decimal_places=2, db_column='horas_periodo')
    proceso_tipo = models.CharField(max_length=1, choices=PROCESO_TIPOS, db_column='tipo_proceso')
    septimo_dia = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='septimo_dia')
    dias_netos = models.DecimalField(max_digits=5, decimal_places=4, db_column='dias_netos')
    septimo_dia_desglosar = models.CharField(default='N', blank=True, null=True, max_length=1, choices=SI_O_NO, db_column='desgl_septimo')
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='es_predet')
    # Otros datos
    isr_tarifa = models.CharField(max_length=1, choices=ISR_TARIFAS, db_column='tarifa_isr')
    isr_tabla_periodo = models.DecimalField(max_digits=5, decimal_places=4, db_column='periodo_tabla_isr')
    isr_ajustar = models.CharField(default='S', max_length=1, choices=SI_O_NO, db_column='hacer_ajuste')
    isr_devolver = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='hacer_devol')  
    isr_retener = models.CharField(default='S', max_length=1, choices=SI_O_NO, db_column='calc_isr')
    imss_retener = models.CharField(default='S', max_length=1, choices=SI_O_NO, db_column='calc_imss')  
    #informacion contable
    cuentacontable_pagos_efectivo = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_pagos_efectivo')
    cuentacontable_pagos_transferencias = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_pagos_trans')
    cuentacontable_pagos_especie = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_pagos_especie')
    poliza_tipo = models.CharField(max_length=1, blank=True, null=True, db_column='tipo_poliza')
    poliza_descripcion = models.CharField(max_length=200, blank=True, null=True, db_column='descripcion_poliza')
    #otros
    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion      = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')
    
    class Meta:
        db_table = u'frecuencias_pago'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.id

class NominaConceptoBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)

    id = models.AutoField(primary_key=True, db_column='concepto_no_id')
    nombre = models.CharField(max_length=50, db_column='nombre')
    nombre_abrev = models.CharField(max_length=50, db_column='nombre_abrev')
    naturaleza = models.CharField(max_length=50, db_column='naturaleza')
    tipo = models.CharField(max_length=50, db_column='tipo')
    clave = models.CharField(max_length=50, db_column='clave')
    id_interno = models.CharField(max_length=1, blank=True, null=True, db_column='id_interno')
    forma_pago = models.CharField(max_length=1, blank=True, null=True, db_column='forma_pago')
    exencion_isr = models.CharField(max_length=1, blank=True, null=True, db_column='exencion_isr')
    percepciones_tipo = models.CharField(max_length=1, blank=True, null=True, db_column='tipo_percep')
    saldo_minimo_excen = models.DecimalField(max_digits=6, decimal_places=2, db_column='salmin_exen')
    percep_var_imss = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='percep_var_imss')
    integracion_imss_tipo = models.CharField(max_length=1, blank=True, null=True, db_column='tipo_integ_imss')
    integracion_imss_no = models.DecimalField(max_digits=5, decimal_places=2, db_column='no_integ_imss')
    
    integracion_ptu = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='integ_ptu')
    integracion_impuesto_estatal = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='integ_impto_estatal')
    tipo_calculo = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='tipo_calc')
    
    pago_unitario = models.DecimalField(default=0, max_digits=18, decimal_places=6, db_column='pago_unitario')
    tabla = models.ForeignKey('NominaTabla', blank=True, null=True, db_column='tabla_no_id',on_delete=models.CASCADE)
    expresion = models.TextField(blank=True, null=True, db_column='expresion')
    funcion = models.TextField(blank=True, null=True, db_column='funcion')
    expresion_min = models.TextField(blank=True, null=True, db_column='expresion_min')
    funcion_min = models.TextField(blank=True, null=True, db_column='funcion_min')
    expresion_max = models.TextField(blank=True, null=True, db_column='expresion_max')
    funcion_max = models.TextField(blank=True, null=True, db_column='funcion_max')
    
    redondeo_particular = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='redondeo_particular')
    factor_redondeo = models.DecimalField(default=0, max_digits=18, decimal_places=6, db_column='factor_redondeo')
    cuenta_contable = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_contable')
    
    #otros
    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion      = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')

    if int(settings.MICROSIP_VERSION) >= 2013:
        tipo_sat = models.IntegerField(blank=True, null=True, db_column='tipo_sat')
        prev_social = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='prev_social')
        simbolo_cuota = models.CharField(max_length=7, db_column='simbolo_cuota')
    
    class Meta:
        db_table = u'conceptos_no'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.nombre_abrev