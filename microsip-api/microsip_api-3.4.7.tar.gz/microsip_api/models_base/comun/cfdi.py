#encoding:utf-8
from django.db import models
from django.conf import settings
from microsip_api.comun.sic_db import next_id

class RepositorioCFDIBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='cfdi_id')
    MODALIDAD_FACTURACION_OPS = (('CFDI','CFDI'), ('CFD','CFD'), ('IMPCBB','IMPCBB'), ('EXT','EXT'))
    modalidad_facturacion = models.CharField(max_length=10, choices=MODALIDAD_FACTURACION_OPS, db_column='MODALIDAD_FACTURACION')
    if int(settings.MICROSIP_VERSION) >= 2017:
        version = models.CharField(max_length=3, db_column='version')
    uuid = models.CharField(max_length=45, db_column='uuid')
    NATURALEZA_OPS = (('E','E'),('R','R'))
    naturaleza = models.CharField(default='E', max_length=1,  choices=NATURALEZA_OPS,db_column='naturaleza')
    TIPO_COMPROBANTE_OPS = (('I','I'),('E','E'))
    tipo_comprobante = models.CharField(default='I', choices=TIPO_COMPROBANTE_OPS, max_length=1,  db_column='tipo_comprobante')
    TIPO_DOCTO_MSP_OPS = (('Factura','Factura'),)
    microsip_documento_tipo = models.CharField(default='I', blank=True, null=True, choices=TIPO_DOCTO_MSP_OPS, max_length=30,  db_column='tipo_docto_msp')
    folio = models.CharField(max_length=45, blank=True, null=True, db_column='folio')
    fecha = models.DateField(db_column='fecha')
    rfc = models.CharField(max_length=13, db_column='rfc', blank=True, null=True)
    taxid = models.CharField(max_length=30, db_column='taxid', blank=True, null=True)
    nombre = models.CharField(max_length=30, db_column='nombre', blank=True, null=True)
    importe = models.DecimalField(max_digits=15, decimal_places=2, db_column='importe')
    moneda = models.CharField(max_length=20, db_column='moneda')
    tipo_cambio = models.DecimalField(default=1, max_digits=18, decimal_places=6, db_column='tipo_cambio')
    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    es_parcialidad = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='es_parcialidad')
    archivo_nombre = models.CharField(max_length=100,  blank=True, null=True, db_column='nom_arch')
    xml = models.TextField(db_column='XML', blank=True, null=True)
    refer_grupo = models.CharField(max_length=30,  blank=True, null=True, db_column='refer_grupo')
    fecha_cancelacion = models.DateField( blank=True, null=True, db_column='fecha_cancelacion')
    SELLO_VALIDADO_OPS = (('M', 'M'),)
    sello_validado = models.CharField(max_length=1, choices=SELLO_VALIDADO_OPS ,db_column='sello_validado')
    usuario_val_sello = models.CharField(max_length=31,  blank=True, null=True, db_column='usuario_val_sello')
    creacion_usuario = models.CharField(max_length=31,  blank=True, null=True, db_column='USUARIO_CREADOR')
    creacion_fechahora = models.DateTimeField(auto_now_add=True,  blank=True, null=True, db_column='FECHA_HORA_CREACION')
    creacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    ultima_modificacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    ultima_modificacion_fechahora = models.DateTimeField(auto_now=True, blank=True, null=True, db_column='FECHA_HORA_ULT_MODIF')
    ultima_modificacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')


    class Meta:
        db_table = u'REPOSITORIO_CFDI'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):
        if self.id == -1 or self.id == None:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(RepositorioCFDIBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(RepositorioCFDIBase, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.id