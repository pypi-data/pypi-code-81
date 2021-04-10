#encoding:utf-8
from django.db import models
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings
from django.db import connections
from django.core import management

class ClienteTipoBase(models.Model):
    id = models.AutoField( primary_key = True, db_column = 'TIPO_CLIENTE_ID' )
    nombre = models.CharField( max_length = 100, db_column = 'NOMBRE' )
     
    class Meta:
        db_table = u'tipos_clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)

class CondicionPagoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='COND_PAGO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    dias_ppag = models.PositiveSmallIntegerField(default=0, db_column='DIAS_PPAG')
    porcentaje_descuento_ppago = models.PositiveSmallIntegerField(default=0, db_column='PCTJE_DSCTO_PPAG')

    SI_O_NO = (('S', 'Si'),('N', 'No'),)
    es_predet = models.CharField(default='N', max_length=1, choices=SI_O_NO ,db_column='ES_PREDET')

    usuario_creador = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    fechahora_creacion = models.DateTimeField(auto_now_add=True, db_column='FECHA_HORA_CREACION')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    fechahora_ult_modif = models.DateTimeField(auto_now = True, db_column='FECHA_HORA_ULT_MODIF')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')
    
    class Meta:
        db_table = u'condiciones_pago'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)

    def save(self, *args, **kwargs):    
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(CondicionPagoBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)

        super(CondicionPagoBase, self).save(*args, **kwargs)


class CondicionPagoPlazoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PLAZO_COND_PAG_ID')
    condicion_de_pago = models.ForeignKey('CondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)
    dias = models.PositiveSmallIntegerField( db_column='DIAS_PLAZO')
    porcentaje_de_venta = models.PositiveSmallIntegerField( db_column='PCTJE_VEN')
    
    class Meta:
        db_table = u'plazos_cond_pag'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):    
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(CondicionPagoPlazoBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)

        super(CondicionPagoPlazoBase, self).save(*args, **kwargs)

class ClienteBase( models.Model ):
    id = models.AutoField( primary_key = True, db_column = 'CLIENTE_ID' )

    nombre = models.CharField( max_length = 100, db_column = 'NOMBRE' )
    contacto1 = models.CharField( max_length = 50, db_column = 'CONTACTO1' )
    estatus = models.CharField( default = 'A',  max_length = 1, db_column = 'ESTATUS' )
    cuenta_xcobrar = models.CharField( max_length = 9, db_column = 'CUENTA_CXC' )
    usuario_ult_modif = models.CharField( blank = True, null = True, max_length = 31, db_column = 'USUARIO_ULT_MODIF' )
    fechahora_ult_modif = models.DateTimeField( auto_now = True, blank = True, null = True, db_column = 'FECHA_HORA_ULT_MODIF' )
    SI_O_NO = (('S', 'Si'),)
    cobrar_impuestos = models.CharField(default='S', max_length=1, choices=SI_O_NO ,db_column='COBRAR_IMPUESTOS')
    generar_interereses = models.CharField(default='S', max_length=1, choices=SI_O_NO ,db_column='GENERAR_INTERESES')
    emir_estado_cuenta = models.CharField(default='S', max_length=1, choices=SI_O_NO ,db_column='EMITIR_EDOCTA')

    moneda = models.ForeignKey('Moneda', db_column = 'MONEDA_ID' ,on_delete=models.CASCADE)
    tipo_cliente = models.ForeignKey( 'ClienteTipo', blank = True, null = True, db_column = 'TIPO_CLIENTE_ID' ,on_delete=models.CASCADE)
    condicion_de_pago = models.ForeignKey('CondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)
    vendedor = models.ForeignKey('Vendedor', db_column='VENDEDOR_ID',on_delete=models.CASCADE)
    zona = models.ForeignKey('Zona', db_column='ZONA_CLIENTE_ID', blank=True, null=True,on_delete=models.CASCADE)
    
    class Meta:
        db_table = u'clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)

    def save(self, *args, **kwargs):    
        if self.id == None:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(ClienteBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)  

        super(ClienteBase, self).save(*args, **kwargs)


class ClienteClaveRolBase(models.Model):
    id      = models.AutoField(primary_key=True, db_column='ROL_CLAVE_CLI_ID')
    nombre  = models.CharField(max_length=50, db_column='NOMBRE')
    es_ppal = models.CharField(default='N', max_length=1, db_column='ES_PPAL')
    
    class Meta:
        db_table = u'roles_claves_clientes'
        abstract = True
        managed= False
        app_label='models_base'

class ClienteClaveBase(models.Model):
    id      = models.AutoField(primary_key=True, db_column='CLAVE_CLIENTE_ID')
    clave   = models.CharField(max_length=20, db_column='CLAVE_CLIENTE')
    cliente = models.ForeignKey('Cliente', db_column='CLIENTE_ID',on_delete=models.CASCADE)
    rol = models.ForeignKey('ClienteClaveRol', db_column='ROL_CLAVE_CLI_ID',on_delete=models.CASCADE)

    class Meta:
        db_table = u'claves_clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.clave)

class ClienteDireccionManager(models.Manager):

    def create_simple(self, **kwargs):
        sql = """
            INSERT INTO dirs_clientes 
                (dir_cli_id, nombre_consig, rfc_curp, calle, nombre_calle, num_exterior, num_interior, colonia, 
                referencia, codigo_postal, email, es_dir_ppal, cliente_id, ciudad_id, estado_id, pais_id)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
        
        using = kwargs.get('using', None)
        nombre_consig = kwargs.get('nombre_consignatario', '')
        rfc_curp = kwargs.get('rfc_curp', '')
        calle = kwargs.get('calle', '')
        nombre_calle = kwargs.get('calle_nombre', '')
        num_exterior = kwargs.get('num_exterior', '')
        num_interior = kwargs.get('num_interior', '')
        colonia = kwargs.get('colonia', '')
        referencia = kwargs.get('referencia', '')
        codigo_postal = kwargs.get('codigo_postal', '')
        email = kwargs.get('email', '')
        es_dir_ppal = kwargs.get('es_ppal', 'S')
        cliente_id = kwargs.get('cliente', None)
        ciudad_id = kwargs.get('ciudad', None)
        estado_id = kwargs.get('estado', None)
        pais_id = kwargs.get('pais', None)

        values_data = [-1, nombre_consig, rfc_curp, calle, nombre_calle, num_exterior, num_interior, colonia, referencia, 
            codigo_postal, email, es_dir_ppal, cliente_id, ciudad_id, estado_id, pais_id]

        curs = connections[using].cursor()
        curs.execute(sql, values_data)
        management.call_command( 'syncdb', database = using, interactive= False)

class ClienteDireccionBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DIR_CLI_ID')
    nombre_consignatario = models.CharField(max_length=18, db_column='NOMBRE_CONSIG')
    rfc_curp = models.CharField(max_length=18, db_column='RFC_CURP', blank=True, null=True)
    
    #Direccion
    calle = models.CharField(blank=True, null=True, max_length=430, db_column='CALLE')
    calle_nombre = models.CharField(blank=True, null=True, max_length=100, db_column='NOMBRE_CALLE')
    numero_exterior = models.CharField(blank=True, null=True, max_length=10, db_column='NUM_EXTERIOR')
    numero_interior = models.CharField(blank=True, null=True, max_length=10, db_column='NUM_INTERIOR')
    colonia = models.CharField(blank=True, null=True, max_length=100, db_column='COLONIA')
    if int(settings.MICROSIP_VERSION) >= 2013:
        poblacion = models.CharField(blank=True, null=True, max_length=100, db_column='POBLACION')
    referencia = models.CharField(blank=True, null=True, max_length=100, db_column='REFERENCIA')
    codigo_postal = models.CharField(blank=True, null=True, max_length=10, db_column='CODIGO_POSTAL')
    email = models.EmailField(blank=True, null=True, db_column='EMAIL')
    es_ppal = models.CharField(default='N', max_length=1, db_column='ES_DIR_PPAL')

    cliente = models.ForeignKey('Cliente', db_column='CLIENTE_ID',on_delete=models.CASCADE)
    ciudad = models.ForeignKey('Ciudad', db_column='CIUDAD_ID',on_delete=models.CASCADE)
    estado = models.ForeignKey('Estado', db_column='ESTADO_ID', blank=True, null=True,on_delete=models.CASCADE)
    pais = models.ForeignKey('Pais', db_column='PAIS_ID', blank=True, null=True,on_delete=models.CASCADE)
    telefono1 = models.CharField(blank=True, null=True, max_length=10, db_column='telefono1')
    telefono2 = models.CharField(blank=True, null=True, max_length=10, db_column='telefono2')
    

    objects = ClienteDireccionManager()
    
    class Meta:
        db_table = u'dirs_clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def save(self, *args, **kwargs):
        if self.id == None:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(ClienteDireccionBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)  
            
        super(ClienteDireccionBase, self).save(*args, **kwargs)

    def __str__( self ):
        return '%s' % (self.calle)


class ZonaBase (models.Model):
    id = models.AutoField(primary_key=True, db_column='ZONA_CLIENTE_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')

    class Meta:
        db_table = u'zonas_clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.nombre)

class LibreClienteBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CLIENTE_ID')
    uso_cfdi=models.CharField(max_length=3,db_column='')
    
    class Meta:
        db_table = u'libres_clientes'
        abstract = True
        managed= False
        app_label='models_base'

    def __str__( self ):
        return '%s' % (self.uso_cfdi)