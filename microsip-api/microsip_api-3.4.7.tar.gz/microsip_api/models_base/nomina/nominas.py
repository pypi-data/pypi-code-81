#encoding:utf-8
from django.db import models
from datetime import datetime
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class NominaNominaBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    TIPOS = (
        ('N', 'Ordinaria'),
        ('L', 'Liquidacion de empleados'),
        ('A', 'Aguinaldos'),
        ('R', 'Reparto de utilidades'),
        ('V', 'Vacaciones'),
        ('S', 'Con aumento de sueldos en el periodo'),
        ('E', 'Extraordinaria'),)

    PROCESO_TIPOS = (
        ('A', 'Automatico'),
    )

    id = models.AutoField(primary_key=True, db_column='nomina_id')
    #General
    frecuencia_pago = models.ForeignKey('NominaFrecuenciaPago', db_column='frepag_id',on_delete=models.CASCADE)
    fecha = models.DateField(db_column='fecha')
    tipo = models.CharField(max_length=1, choices=TIPOS, db_column='tipo_nom')
    conceptos_periodicos_suspender = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='suspender_conrep')
    periodo_dias = models.DecimalField(max_digits=5, decimal_places=2, db_column='dias_periodo')
    a_cotizar_dias = models.DecimalField(max_digits=7, decimal_places=4, db_column='dias_a_cot')
    pago_tipo = models.CharField(max_length=1, blank=True, null=True, db_column='tipo_pago')
    periodo_horas = models.DecimalField(max_digits=5, decimal_places=2, db_column='horas_periodo')
    proceso_tipo = models.CharField(max_length=1, choices=PROCESO_TIPOS, db_column='tipo_proceso')
    #Aguinaldo
    AGUINALDO_METODOS = (('F','F'),('D','D'),)
    aguinaldo_concepto  = models.IntegerField(blank=True, null=True, db_column='CONCEPTO_AGUI_ID')
    aguinaldo_metodo = models.CharField(max_length=1, choices=AGUINALDO_METODOS, db_column='METODO_AGUI')
    aguinaldo_faltas = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='FALTAS_AGUI')
    #ptu
    ptu_concepto  = models.IntegerField(blank=True, null=True, db_column='concepto_ptu_id')
    ptu_reparto_importe = models.DecimalField(default=0, max_digits=5, decimal_places=2, db_column='importe_reparto_ptu')
    ptu_ingresos_porcentaje =  models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='pctje_ingresos_ptu')
    ptu_trabajo_minimo_dias = models.PositiveSmallIntegerField(default=0, db_column='dias_trab_min_ptu')
    ptu_ingreso_maximo = models.DecimalField(default=0, max_digits=5, decimal_places=2, db_column='ingreso_max_ptu')
    #vacaciones
    primavacacional_concepto = models.IntegerField(blank=True, null=True, db_column='concepto_pmavac_id')
    vacaciones_descripcion = models.CharField(max_length=200, blank=True, null=True, db_column='descripcion_vac')
    indemnizacion_concepto = models.IntegerField(blank=True, null=True, db_column='concepto_indem_id')
    pmaant_concepto = models.IntegerField(blank=True, null=True, db_column='concepto_pmaant_id')
    #otros
    aplicado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='aplicado')
    contabilizado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='contabilizado')
    integ_ba = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='integ_ba')

    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion      = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')
    
    def _get_tipo_nomina_descripcion(self):
        for tipo in self.TIPOS:
            if tipo[0] == self.tipo:
                return tipo [1]
        return ''

    tipo_nomina_descripcion = property(_get_tipo_nomina_descripcion)
    
    class Meta:
        db_table = u'nominas'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s %s'% (self.fecha, self.tipo_nomina_descripcion)

class NominaNominaPagoBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    NOMINA_TIPOS = (
        ('N', 'Ordinaria'),
        ('L', 'Liquidación de empleados'),
        ('A', 'Aguinaldos'),
        ('R', 'Reparto de utilidades'),
        ('V', 'Vacaciones'),
        ('S', 'Con aumento de sueldos en el periodo'),
        ('E', 'Extraordinaria'),
    )

    id = models.AutoField(primary_key=True, db_column='pago_nomina_id')
    #General
    nomina = models.ForeignKey('NominaNomina', db_column='nomina_id',on_delete=models.CASCADE)
    empleado = models.ForeignKey('NominaEmpleado', db_column='empleado_id',on_delete=models.CASCADE)
    trabajo_dias = models.DecimalField(max_digits=7, decimal_places=2, db_column='dias_trab')
    trabajo_horas = models.DecimalField(max_digits=7, decimal_places=2, db_column='horas_trab')
    
    vacaciones_dias = models.DecimalField(max_digits=7, decimal_places=2, db_column='dias_vac')
    cotizacion_dias = models.DecimalField(max_digits=9, decimal_places=4, db_column='dias_cot')
    faltas = models.CharField(max_length=5, db_column='faltas')
    faltas_dec = models.DecimalField(max_digits=7, decimal_places=2, db_column='faltas_dec')
    aus_imss_dias = models.PositiveSmallIntegerField(default=0, db_column='dias_aus_imss')
    incapacidad_dias = models.PositiveSmallIntegerField(default=0, db_column='dias_incap')
    #horas extra
    horas_extra = models.CharField(max_length=4, db_column='horas_ext')
    horas_extra_dec = models.DecimalField(max_digits=7, decimal_places=2, db_column='horas_ext_dec')
    horas_extra_exced = models.DecimalField(max_digits=7, decimal_places=2, db_column='horas_ext_exced')
    horas_extra_exced_importe = models.DecimalField(max_digits=15, decimal_places=2, db_column='importe_horas_ext_exced')

    horas_especiales = models.CharField(max_length=4, db_column='horas_esp')
    horas_especiales_dec = models.DecimalField(max_digits=7, decimal_places=2, db_column='horas_esp_dec')
    #sbc
    sbc_smdf = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_smdf')
    sbc_exced = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_exced')
    sbc_din = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_din')
    sbc_iv_cv = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_iv_cv')
    sbc_retiro = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_retiro')
    sbc_riesgo = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_riesgo')
    sbc_infon = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='sbc_infon')
    total_percep = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_percep')
    total_reten = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_reten')
    total_percep_especie = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_percep_especie')
    total_reten_deduc = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_reten_deduc')
    total_percep_grav = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_percep_grav')
    total_percep_exen = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_percep_exen')
    total_percep_no_acum = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_percep_no_acum')
    total_tipo_a = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_tipo_a')
    total_tipo_b = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_tipo_b')
    total_tipo_c = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='total_tipo_c')
    base_ptu = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='base_ptu')
    base_impto_estatal = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='base_impto_estatal')
    cas_aplicado = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='cas_aplicado')

    fecha = models.DateField(db_column='fecha')
    nomina_tipo = models.CharField(max_length=1, choices=NOMINA_TIPOS, db_column='tipo_nom')
    pago_forma = models.CharField(max_length=1, choices=NOMINA_TIPOS, db_column='forma_pago')
    pago_tipo = models.CharField(max_length=1, choices=NOMINA_TIPOS, db_column='tipo_pago')
    
    aplicado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='aplicado')
    forma_emitida = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='forma_emitida')
    
    if int(settings.MICROSIP_VERSION) >= 2013:
        envio_enviado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='enviado')
        envio_email = models.EmailField(blank=True, null=True, db_column='email_envio')                                        
        envio_fechahora = models.DateTimeField( blank=True, null=True, db_column='fecha_hora_envio')                            
        cfdi_certificado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='cfdi_certificado')
    
    integ_ba = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='integ_ba')
    contabilizado_ba = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='contabilizado_ba')

    cuentacontable_banco = models.CharField(max_length=9, blank=True, null=True, db_column='cuenta_ban_id')
    cheque_numero = models.CharField(blank=True, null=True, max_length=9, db_column='num_cheque')
    pago_electronico_generado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='pago_elect_generado')
    pago_electronico_cuentabancaria = models.CharField(blank=True, null=True, max_length=9, db_column='num_ctaban_pago_elect')

    usuario_creador         = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion      = models.DateTimeField(auto_now_add=True, db_column='fecha_hora_creacion')
    usuario_aut_creacion    = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif     = models.DateTimeField(auto_now = True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif       = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')
    
    class Meta:
        db_table = u'pagos_nomina'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.id

class NominaNominaPagoDetalleBase(models.Model):
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    id = models.AutoField(primary_key=True, db_column='pago_nomina_det_id')
    #General
    nomina_pago = models.ForeignKey('NominaNominaPago', related_name="detalles", db_column='pago_nomina_id',on_delete=models.CASCADE)
    concepto = models.ForeignKey('NominaConcepto', db_column='concepto_no_id',on_delete=models.CASCADE)
    
    cuota = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='cuota')
    ahorro_empresa = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='ahorro_empresa')
    prestamo = models.ForeignKey('NominaPrestamo', blank=True, null=True, db_column='prestamo_emp_id',on_delete=models.CASCADE)
    unidades = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='unidades')
    importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='importe')
    importe_gravable = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='importe_gravable')
    importe_exento = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='importe_exento')
    importe_ahorro_empresa = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='importe_ahorro_empresa')
    acumulable = models.CharField(default='S', max_length=1, choices=SI_O_NO, db_column='acumulable')
    empleado = models.ForeignKey('NominaEmpleado', db_column='empleado_id',on_delete=models.CASCADE)
    aplicado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='aplicado')
    
    class Meta:
        db_table = u'pagos_nomina_det'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__( self ):
        return u'%s'% self.id