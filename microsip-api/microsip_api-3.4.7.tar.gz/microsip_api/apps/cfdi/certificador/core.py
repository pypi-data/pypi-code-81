#encoding:utf-8
import codecs
import os
import sys
import xlrd

from microsip_api.comun.comun_functions import split_letranumero, concatenar_conceptos, get_long_folio
from microsip_api.apps.cfdi.core import CertificadoDigital, ClavesComercioDigital
from microsip_api.comun.sic_db import first_or_none
from datetime import datetime
import xml.etree.cElementTree as ET
from django.core import management
from django.db import connections, transaction


class CertificadorSAT():
    def __init__(self, sellos_folder_path,**kwargs):
        self.sellos_folder_path = sellos_folder_path
        self.api_folder_path = "%s\\comercio_digital\\"%os.path.dirname(os.path.realpath(__file__))
        self.modo = kwargs.get('modo', 'PRUEBAS')
        if self.modo != 'PROD':
            self.modo = 'PRUEBAS'
            
        self.passwords = ClavesComercioDigital("%s\\comercio_digital_claves.xlsx"%self.sellos_folder_path)
        self.errors = []

    def certificar(self, **kwargs):
        ini_file_path = kwargs.get('ini_file_path', "%sFT-001.ini"%self.api_folder_path )
        rfc = kwargs.get('rfc', 'AAA010101AAA')
        empresa_folder_name = kwargs.get('empresa_folder_name', rfc)
        
        try:
            password = self.passwords[rfc]
        except KeyError:
            if rfc == 'AAA010101AAA':
                password = 'PWD'
            else:
                password = None
                self.errors.append('no se encontro password')

        certificado_digital = CertificadoDigital("%s\\sellos\\%s"%(self.sellos_folder_path, empresa_folder_name))
        
        if certificado_digital.errors:
            self.errors += certificado_digital.errors

        if not certificado_digital.errors and password:
            comando = '%s %s %s %s %s %s %s %s NO'%(
                "%scd_sellar.exe"%self.api_folder_path,
                rfc,
                password,
                ini_file_path,
                certificado_digital.certificado_key, 
                certificado_digital.certificado_cer, 
                certificado_digital.password,
                self.modo
            )

        if not self.errors:
            os.system(comando)

        try:
            print ('%s.sat'%ini_file_path)
            sat_file = codecs.open('%s.sat'%ini_file_path, encoding='utf-8')
        except IOError:
            self.errors.append('Problema al generar archivo [.sat]')
        else:
            lineas = sat_file.readlines()
            sat_file.close()

            if lineas[0] != u'1\n':
                try:
                    self.errors.append(lineas[1])
                except IndexError:
                    self.errors.append("Error en certificado probablemente esta vacio")
        return self.errors

    def certificar_33(self, **kwargs):
        ini_file_path = kwargs.get('ini_file_path', "%sFT-001.ini"%self.api_folder_path )
        rfc = kwargs.get('rfc', 'AAA010101AAA')
        empresa_folder_name = kwargs.get('empresa_folder_name', rfc)
        
        try:
            password = self.passwords[rfc]
        except KeyError:
            if rfc == 'AAA010101AAA':
                password = 'PWD'
            else:
                password = None
                self.errors.append('no se encontro password')

        certificado_digital = CertificadoDigital("%s\\sellos\\%s"%(self.sellos_folder_path, empresa_folder_name))
        
        if certificado_digital.errors:
            self.errors += certificado_digital.errors


        if not certificado_digital.errors and password:
            comando = '%s %s %s %s %s %s %s %s %s'%(
                "%ssellaTimbra33.exe"%self.api_folder_path.replace("comercio_digital","comercio_digital33"),
                rfc,
                password,
                ini_file_path,
                'WS',
                'SI',
                certificado_digital.password,
                certificado_digital.certificado_key, 
                certificado_digital.certificado_cer, 
            )
            print (comando)
        if not self.errors:
            os.system(comando)

        try:
            print ('%s.sat'%ini_file_path)
            sat_file = codecs.open('%s.sat'%ini_file_path, encoding='utf-8')

        except IOError as er:
            self.errors.append('Problema al generar archivo [.sat]')
        else:
            lineas = sat_file.readlines()
            sat_file.close()
            if lineas[0] != u'OK':
                try:
                    self.errors.append(lineas[1])
                except IndexError:
                    self.errors.append("Error en certificado probablemente esta vacio")
        return self.errors

def create_ini_file(documento_id, sellos_folder_path, facturar_a, using):
    'Funcion para certificar una factura.'
    from django_microsip_base.libs.models_base.models import VentasDocumento, Registry, Cliente, ClienteDireccion, Ciudad, Estado, Pais, VentasDocumentoDetalle, Articulo

    documento = VentasDocumento.objects.using(using).filter(pk=documento_id).values()[0]
    xml_data = []
    serie, folio = split_letranumero(documento['folio'])
    subtotal = documento['importe_neto'] - documento['otros_cargos'] - documento['impuestos_total'] - documento['retenciones_total']- documento['fpgc_total']

    #Comprobante
    xml_data.append([
        'Comprobante',[
            ['Version', '3.2'],
            ['TipoDeComprobante', 'ingreso'],
            ['Serie', serie],
            ['Folio', folio],
            ['Fecha', documento['fecha']],
            ['FormaDePago', 'Pago en una sola exhibicion'],
            ['CondicionesDePago', 'Contado'],
            ['SubTotal', subtotal],
            # 'Descuento', descuento_importe],
            # 'MotivoDescuento', 'No aplica'],
            ['TipoCambio',  documento['tipo_cambio']],
            ['Moneda', 'MXN'],
            ['Total', documento['importe_neto']],
            ['MetodoDePago', 'No aplica'],
            ['LugarExpedicion',  'CUAUHTEMOC, CHIHUAHUA'],
            # ['NumCtaPago', 'No aplica'],
        ]
    ])
    
    #Emisor
    datos_empresa = Registry.objects.using(using).get(nombre='DatosEmpresa')
    datos_empresa = Registry.objects.using(using).filter(padre=datos_empresa)
    
    datos_emisor = {
        'Rfc': datos_empresa.get(nombre='Rfc').get_value().replace('-','').replace(' ',''),
        'Nombre': datos_empresa.get(nombre='Nombre').get_value(),
        'RegimenFiscal':datos_empresa.get(nombre='RegimenFiscal').get_value() or '',
        'Calle': datos_empresa.get(nombre='NombreCalle').get_value() or '',
        'NoExterior': datos_empresa.get(nombre='NumExterior').get_value() or '',
        'NoInterior': datos_empresa.get(nombre='NumInterior').get_value() or '',
        'Colonia': datos_empresa.get(nombre='Colonia').get_value() or '',
        # 'Localidad': datos_empresa.get(nombre='Nombre').get_value(),
        'Referencia': datos_empresa.get(nombre='Referencia').get_value() or '',
        'Municipio': datos_empresa.get(nombre='Ciudad').get_value() or '',
        'Estado': datos_empresa.get(nombre='Estado').get_value() or '',
        'Pais': datos_empresa.get(nombre='Pais').get_value() or '',
        'CodigoPostal': datos_empresa.get(nombre='CodigoPostal').get_value() or '',
    }
    
    xml_data.append([
        'Emisor',[  
            ['Rfc', datos_emisor['Rfc']],
            ['Nombre', datos_emisor['Nombre']],
            ['RegimenFiscal', datos_emisor['RegimenFiscal']],
            ['Calle', datos_emisor['Calle']],
            ['NoExterior', datos_emisor['NoExterior']],
            ['NoInterior', datos_emisor['NoInterior']],
            ['Colonia', datos_emisor['Colonia']],
            # ['Localidad', datos_emisor['Localidad']],
            ['Referencia', datos_emisor['Referencia']],
            ['Municipio', datos_emisor['Municipio']],
            ['Estado', datos_emisor['Estado']],
            ['Pais', datos_emisor['Pais']],
            ['CodigoPostal', datos_emisor['CodigoPostal']]
        ]
    ])
   
    #Receptor
    cliente = Cliente.objects.using(using).get(pk=documento['cliente_id'])
    direccion_cliente = ClienteDireccion.objects.using(using).filter(pk=documento['cliente_direccion_id']).values()[0]
    
    poblacion = ''
    if 'poblacion' in direccion_cliente:
        poblacion = direccion_cliente['poblacion']

    xml_data.append([
        'Receptor',[  
            ['Rfc', direccion_cliente['rfc_curp'].replace('-','').replace(' ','')],
            ['Nombre', cliente.nombre],
            ['Calle', direccion_cliente['calle_nombre']],
            ['NoExterior', direccion_cliente['numero_exterior']],
            ['NoInterior', direccion_cliente['numero_interior']],
            ['Colonia', direccion_cliente['colonia']],
            ['Localidad', poblacion],
            ['Referencia', direccion_cliente['referencia']],
            ['Municipio', Ciudad.objects.using(using).get(pk=direccion_cliente['ciudad_id']).nombre],
            ['Estado',Estado.objects.using(using).get(pk=direccion_cliente['estado_id']).nombre],
            ['Pais', Pais.objects.using(using).get(pk=direccion_cliente['pais_id']).nombre ],
            ['CodigoPostal', direccion_cliente['codigo_postal']],
        ]
    ])

    #Conceptos
    xml_articulos_data = []
    detalles = VentasDocumentoDetalle.objects.using(using).filter(documento__id=documento['id']).values()
    contador = 0
    for detalle in detalles:
        contador = contador + 1
        articulo = Articulo.objects.using(using).get(pk=detalle['articulo_id'])
        xml_articulos_data.append([
            'Concepto%s'%contador,[  
                ['Cantidad', detalle['unidades']],
                ['Unidad', articulo.unidad_venta],
                ['NoIdentificacion', facturar_a['articulo_clave']],
                ['Descripcion', articulo.nombre],
                ['ValorUnitario', detalle['precio_unitario']],
                ['Importe', detalle['precio_total_neto']],
            ]
        ])

    xml_data.append(['list', xml_articulos_data])

    #Impuestos
    xml_data.append([
        'Impuestos',[  
            ['TotalImpuestosTrasladados', '0'],
            ['IEPSTrasladado', '0'],
            ['IEPSTasa', '0'],
            ['IVATrasladado', '0'],
            ['IVATasa', '0'],
        ]
    ])

    import codecs
    
    ruta_archivo_ini = u"%s\\facturas\\%s.ini"%(sellos_folder_path, documento['folio'])

    archivo = codecs.open(ruta_archivo_ini, encoding='utf-8', mode='w+')
    
    for encabezado in xml_data:
        if encabezado[0] == 'list':
            for grupo_datos in encabezado[1]:
                archivo.write( concatenar_conceptos(grupo_datos) )    
        else:   
            archivo.write( concatenar_conceptos(encabezado) )         
            
    archivo.close()

def save_xml_in_document(ruta_archivo_ini, using, documento_id):
    from django_microsip_base.libs.models_base.models import ConfiguracionFolioFiscalUso, VentasDocumento

    sat_file = codecs.open('%s.sat'%ruta_archivo_ini, encoding='utf-8')
    lineas = sat_file.readlines()
    sat_file.close()
    
    if lineas[0]==u'1\n':
        uuid = (lineas[1].replace('\n','').split('='))[1]
        xml_file = codecs.open('%s.xml'%ruta_archivo_ini, encoding='utf-8')
        xml = ''
        for linea in xml_file:
            xml = xml + linea
        xml_file.close()
        
        uso_folios_fiscales = ConfiguracionFolioFiscalUso.objects.using(using).get(documento= documento_id)
        uso_folios_fiscales.xml = xml
        uso_folios_fiscales.prov_cert = 'CDIGITAL'
        uso_folios_fiscales.fechahora_timbrado = datetime.now().strftime("%Y-%m-%dT%I:%M:%S")
        uso_folios_fiscales.uuid = uuid
        uso_folios_fiscales.save(using=using,update_fields=['xml','prov_cert', 'fechahora_timbrado', 'uuid',])
        
        documento = VentasDocumento.objects.using(using).get(pk=documento_id)
        documento.cfd_certificado = 'S'
        documento.aplicado = 'S'
        documento.save(using=using, update_fields=['cfd_certificado','aplicado',]) 

        os.remove(ruta_archivo_ini)
        os.remove('%s.sat'%ruta_archivo_ini)
        os.remove('%s.xml'%ruta_archivo_ini)


#  *********************** PARA FACTURACION 3.3 Y DOCUMENTOS EN PUNTO DE VENTA (APLICACION DE FACTURACION EN LINEA) ********************************

def create_ini_file_33_pv(documento_id, sellos_folder_path, using):
    'Funcion para certificar una factura.'
    from django_microsip_base.libs.models_base.models import PuntoVentaDocumento, Registry, Cliente, ClienteDireccion, Ciudad, Estado, Pais, PuntoVentaDocumentoDetalle, Articulo, ArticuloClave

    documento = PuntoVentaDocumento.objects.using(using).filter(pk=documento_id).values()[0]
    xml_data = []
    serie, folio = split_letranumero(documento['folio'])
    subtotal = documento['importe_neto']

    
    #Comprobante
    comprobante = ET.Element("cfdi:Comprobante")
    emisor = ET.SubElement(comprobante,"cfdi:Emisor")
    receptor = ET.SubElement(comprobante,"cfdi:Receptor")
    conceptos = ET.SubElement(comprobante,"cfdi:Conceptos")
    impuestos = ET.SubElement(comprobante,"cfdi:Impuestos")

    comprobante.set('Version', '3.3')
    comprobante.set('TipoDeComprobante', 'I')
    comprobante.set('Serie', serie)
    comprobante.set('Folio', str(folio))
    comprobante.set('Fecha', datetime.now().strftime("%Y-%m-%dT%I:%M:%S"))
    comprobante.set('FormaPago', '01')
    comprobante.set('CondicionesDePago', 'Contado')
    comprobante.set('MetodoPago', 'PUE')
    comprobante.set('SubTotal', str(subtotal))
    comprobante.set('TipoCambio',  '1')
    comprobante.set('Moneda', 'MXN')
    comprobante.set('Total', str(documento['importe_neto'] + documento['total_impuestos']))
    comprobante.set('LugarExpedicion',  '31510')
    comprobante.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    comprobante.set('xmlns:cfdi', 'http://www.sat.gob.mx/cfd/3')
    comprobante.set('xsi:schemaLocation', 'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd')
    
    #Emisor
    datos_empresa = Registry.objects.using(using).get(nombre='DatosEmpresa')
    datos_empresa = Registry.objects.using(using).filter(padre=datos_empresa)
    
    emisor.set('Rfc',datos_empresa.get(nombre='Rfc').get_value().replace('-','').replace(' ',''))
    emisor.set('Nombre',datos_empresa.get(nombre='Nombre').get_value())
    emisor.set('RegimenFiscal','601')

  
    #Receptor
    cliente = Cliente.objects.using(using).get(pk=documento['cliente_id'])
    direccion_cliente = ClienteDireccion.objects.using(using).filter(pk=documento['direccion_cliente_id']).values()[0]
    
    poblacion = ''
    if 'poblacion' in direccion_cliente:
        poblacion = direccion_cliente['poblacion']

    receptor.set('Rfc',direccion_cliente['rfc_curp'].replace('-','').replace(' ',''))
    receptor.set('Nombre',cliente.nombre)
    receptor.set('UsoCFDI','G01')

    #Conceptos
    xml_articulos_data = []
    detalles = PuntoVentaDocumentoDetalle.objects.using(using).filter(documento_pv__id=documento['id']).values()
    contador = 0
    for detalle in detalles:
        contador = contador + 1
        articulo = Articulo.objects.using(using).get(pk=detalle['articulo_id'])
        clave = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
        # c.execute()
        # ********** SACAR LA CLAVE DEL SAT DEL ARTICULO Y LA CLAVE DE LA UNIDAD DE MEDIDA
        concepto = ET.SubElement(conceptos,"cfdi:Concepto")
        concepto.set('Cantidad',str(detalle['unidades']))
        concepto.set('ClaveUnidad','A91')
        concepto.set('Unidad',articulo.unidad_venta)
        concepto.set('Descripcion', articulo.nombre)
        concepto.set('ValorUnitario',str(detalle['precio_unitario']))
        concepto.set('Importe',str(detalle['precio_total_neto']))
        concepto.set('ClaveProdServ','49161603')
        impuesto_det = ET.SubElement(concepto,"cfdi:Impuestos")
        traslados_impto = ET.SubElement(impuesto_det,"cfdi:Traslados")
        traslados_det = ET.SubElement(traslados_impto,"cfdi:Traslado")
        traslados_det.set('Base',str(detalle['precio_total_neto']))
        traslados_det.set('Impuesto','002')
        traslados_det.set('TipoFactor','Tasa')
        traslados_det.set('TasaOCuota','0.16')
        traslados_det.set('Importe', str((float(detalle['precio_total_neto'])*0.16)))


      
    #Impuestos
    impuestos.set('TotalImpuestosTrasladados',str(documento['total_impuestos']))
    impuesto_hijo = ET.SubElement(impuestos,"cfdi:Traslados")
    impuesto_hijo_det = ET.SubElement(impuesto_hijo,"cfdi:Traslado")
    impuesto_hijo_det.set('Impuesto','002')
    impuesto_hijo_det.set('TipoFactor','Tasa')
    impuesto_hijo_det.set('TasaOCuota','0.16')
    impuesto_hijo_det.set('Importe',str(documento['total_impuestos']))

    import codecs
    
    ruta_archivo_ini = u"%s\\facturas\\%s.ini"%(sellos_folder_path, documento['folio'])
    reload(sys)  
    sys.setdefaultencoding('utf8')
    archivo = codecs.open(ruta_archivo_ini, encoding='UTF-8', mode='w+')
    xmlstr = ET.tostring(comprobante,encoding='UTF-8', method='xml').replace("<?xml version='1.0' encoding='UTF-8'?>",'<?xml version="1.0" encoding="UTF-8"?>')
    xmlstr = xmlstr.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    xmlstr = xmlstr.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')      
    archivo.write(xmlstr)        
    archivo.close()


def save_xml_in_document_33_pv(ruta_archivo_ini, using, facturar_a_documento_id):
    from django_microsip_base.libs.models_base.models import ConfiguracionFolioFiscalUso, PuntoVentaDocumento, RepositorioCFDI
    
    xml_file = codecs.open('%s.xml'%ruta_archivo_ini, encoding='utf-8')
    xml = ''
    for linea in xml_file:
        xml = xml + linea
    xml_file.close()

    tree=ET.parse('%s.xml'%ruta_archivo_ini)
    root = tree.getroot()
    comp = root.find('{http://www.sat.gob.mx/cfd/3}Complemento')
    receptor = root.find('{http://www.sat.gob.mx/cfd/3}Receptor')
    emisor = root.find('{http://www.sat.gob.mx/cfd/3}Emisor')
    uuid = comp.find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital').attrib['UUID']
    rfc_receptor = receptor.attrib['Rfc']
    nombre_receptor = receptor.attrib['Nombre']
    xml_total = root.attrib['Total']
    rfc_emisor = emisor.attrib['Rfc']
    fecha_formato = datetime.now().strftime("%Y%m%d")

    
    documento = PuntoVentaDocumento.objects.using(using).get(pk=documento_id)
    documento.cfdi_certificado = 'S'
    documento.aplicado = 'S'
    documento.save(using=using, update_fields=['cfdi_certificado','aplicado',])


    serie,folio = split_letranumero(documento.folio)

    rep  = RepositorioCFDI.objects.create(
        id = -1,
        modalidad_facturacion = 'CFDI',
        version = '3.3',
        uuid = uuid,
        naturaleza = 'E',
        tipo_comprobante = 'I',
        microsip_documento_tipo = 'Factura',
        folio = '%s%s'%(serie,folio),
        fecha = datetime.now(),
        rfc = rfc_receptor,
        taxid = None,
        nombre = nombre_receptor,
        importe = xml_total  ,
        moneda = 'MXN',
        tipo_cambio = 1,
        es_parcialidad = 'N',
        archivo_nombre = '%s_Factura_%s%s_%s.xml'%(rfc_emisor,serie,folio,fecha_formato),
        xml = xml,
        sello_validado = 'M')

    # ll
    uso_folios_fiscales = ConfiguracionFolioFiscalUso.objects.using(using).get(documento= documento_id)
    uso_folios_fiscales.xml = xml
    uso_folios_fiscales.prov_cert = 'CDIGITAL'
    uso_folios_fiscales.fechahora_timbrado = datetime.now().strftime("%Y-%m-%dT%I:%M:%S")
    uso_folios_fiscales.uuid = uuid
    uso_folios_fiscales.documento = documento.id
    uso_folios_fiscales.cfdi = rep.id

    uso_folios_fiscales.save(using=using,update_fields=['xml','prov_cert', 'fechahora_timbrado', 'uuid', 'documento','cfdi'])
    management.call_command( 'syncdb', database = using, interactive=False)

    os.remove(ruta_archivo_ini)
    os.remove('%s.sat'%ruta_archivo_ini)
    # os.remove('%s.xml'%ruta_archivo_ini)


# **************** PARA FACTURACION 3.3 Y DOCUMENTOS DE VENTAS**********************
def create_ini_file_33_ve(documento_id, sellos_folder_path, using):
    'Funcion para certificar una factura.'
    from django_microsip_base.libs.models_base.models import VentasDocumento, Registry, Cliente, ClienteDireccion, Ciudad, Estado, Pais, VentasDocumentoDetalle, Articulo,ArticuloClave

    c = connections[using].cursor()
    documento = VentasDocumento.objects.using(using).filter(pk=documento_id).values()[0]
    xml_data = []
    serie, folio = split_letranumero(documento['folio'])
    subtotal = documento['importe_neto']

    
    #Comprobante
    comprobante = ET.Element("cfdi:Comprobante")
    emisor = ET.SubElement(comprobante,"cfdi:Emisor")
    receptor = ET.SubElement(comprobante,"cfdi:Receptor")
    conceptos = ET.SubElement(comprobante,"cfdi:Conceptos")
    impuestos = ET.SubElement(comprobante,"cfdi:Impuestos")

    comprobante.set('Version', '3.3')
    comprobante.set('TipoDeComprobante', 'I')

    if len(serie)>0:
        comprobante.set('Serie', serie)
    comprobante.set('Folio', str(folio))
    comprobante.set('Fecha', datetime.now().strftime("%Y-%m-%dT%I:%M:%S"))
    comprobante.set('FormaPago', '99')
    comprobante.set('CondicionesDePago', 'Credito')
    comprobante.set('MetodoPago', 'PPD')
    comprobante.set('SubTotal', str(subtotal))
    comprobante.set('TipoCambio',  '1')
    comprobante.set('Moneda', 'MXN')
    comprobante.set('Total', str(documento['importe_neto'] + documento['impuestos_total']))
    comprobante.set('LugarExpedicion',  '31500')
    comprobante.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    comprobante.set('xmlns:cfdi', 'http://www.sat.gob.mx/cfd/3')
    comprobante.set('xsi:schemaLocation', 'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd')
    
    #Emisor
    datos_empresa = Registry.objects.using(using).get(nombre='DatosEmpresa')
    datos_empresa = Registry.objects.using(using).filter(padre=datos_empresa)
    
    emisor.set('Rfc',datos_empresa.get(nombre='Rfc').get_value().replace('-','').replace(' ',''))
    emisor.set('Nombre',datos_empresa.get(nombre='Nombre').get_value())
    emisor.set('RegimenFiscal','612')
    # emisor.set('RegimenFiscal','601')

  
    #Receptor
    cliente = Cliente.objects.using(using).get(pk=documento['cliente_id'])
    direccion_cliente = ClienteDireccion.objects.using(using).filter(pk=documento['cliente_direccion_id']).values()[0]
    
    poblacion = ''
    if 'poblacion' in direccion_cliente:
        poblacion = direccion_cliente['poblacion']

    receptor.set('Rfc',direccion_cliente['rfc_curp'].replace('-','').replace(' ',''))
    receptor.set('Nombre',cliente.nombre)
    receptor.set('UsoCFDI','G03')

    #Conceptos
    xml_articulos_data = []
    detalles = VentasDocumentoDetalle.objects.using(using).filter(documento__id=documento['id']).values()
    contador = 0
    for detalle in detalles:
        contador = contador + 1
        articulo = Articulo.objects.using(using).get(pk=detalle['articulo_id'])
        clave = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
        # ************ CLAVE DE ARTICULO DEL SAT**************************************************
        c.execute("select clave from datos_adicionales where elem_id = %s"%(detalle['articulo_id']))
        claveprodserv = c.fetchall()[0][0]
        # ********** CLAVE DE LA UNIDAD DE MEDIDA**************************************************
        c.execute("select clave_sat from unidades_venta where UNIDAD_VENTA = (select unidad_venta from articulos where articulo_id = %s)"%(detalle['articulo_id']))
        claveunidadmedida = c.fetchall()[0][0]

        concepto = ET.SubElement(conceptos,"cfdi:Concepto")
        concepto.set('Cantidad',str(detalle['unidades']))
        concepto.set('ClaveUnidad',claveunidadmedida)
        concepto.set('Unidad',articulo.unidad_venta)
        concepto.set('Descripcion', articulo.nombre)
        concepto.set('ValorUnitario',str(detalle['precio_unitario']))
        concepto.set('Importe',str(detalle['precio_total_neto']))
        concepto.set('ClaveProdServ',claveprodserv)
        impuesto_det = ET.SubElement(concepto,"cfdi:Impuestos")
        traslados_impto = ET.SubElement(impuesto_det,"cfdi:Traslados")
        traslados_det = ET.SubElement(traslados_impto,"cfdi:Traslado")
        traslados_det.set('Base',str(detalle['precio_total_neto']))
        traslados_det.set('Impuesto','002')
        traslados_det.set('TipoFactor','Exento')
        # traslados_det.set('TasaOCuota','0.16')
        # traslados_det.set('Importe', str((float(detalle['precio_total_neto'])*0.16)))


      
    #Impuestos
    # impuestos.set('TotalImpuestosTrasladados',str(documento['impuestos_total']))
    # impuesto_hijo = ET.SubElement(impuestos,"cfdi:Traslados")
    # impuesto_hijo_det = ET.SubElement(impuesto_hijo,"cfdi:Traslado")
    # impuesto_hijo_det.set('Impuesto','002')
    # impuesto_hijo_det.set('TipoFactor','Exento')
    # impuesto_hijo_det.set('TasaOCuota','0.16')
    # impuesto_hijo_det.set('Importe',str(documento['impuestos_total']))

    import codecs
    
    ruta_archivo_ini = u"%s\\facturas\\%s.ini"%(sellos_folder_path, documento['folio'])
    reload(sys)  
    sys.setdefaultencoding('utf8')
    archivo = codecs.open(ruta_archivo_ini, encoding='UTF-8', mode='w+')
    xmlstr = ET.tostring(comprobante,encoding='UTF-8', method='xml').replace("<?xml version='1.0' encoding='UTF-8'?>",'<?xml version="1.0" encoding="UTF-8"?>')
    xmlstr = xmlstr.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    xmlstr = xmlstr.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')      
    archivo.write(xmlstr)        
    archivo.close()


def save_xml_in_document_33_ve(ruta_archivo_ini, using, documento_id):
    from django_microsip_base.libs.models_base.models import ConfiguracionFolioFiscal, ConfiguracionFolioFiscalUso, VentasDocumento, RepositorioCFDI
    
    xml_file = codecs.open('%s.xml'%ruta_archivo_ini, encoding='utf-8')
    xml = ''
    for linea in xml_file:
        xml = xml + linea
    xml_file.close()

    tree=ET.parse('%s.xml'%ruta_archivo_ini)
    root = tree.getroot()
    comp = root.find('{http://www.sat.gob.mx/cfd/3}Complemento')
    receptor = root.find('{http://www.sat.gob.mx/cfd/3}Receptor')
    emisor = root.find('{http://www.sat.gob.mx/cfd/3}Emisor')
    uuid = comp.find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital').attrib['UUID']
    rfc_receptor = receptor.attrib['Rfc']
    nombre_receptor = receptor.attrib['Nombre']
    xml_total = root.attrib['Total']
    rfc_emisor = emisor.attrib['Rfc']
    fecha_formato = datetime.now().strftime("%Y%m%d")

    
    documento = VentasDocumento.objects.using(using).get(pk=documento_id)
    documento.cfd_certificado = 'S'
    documento.aplicado = 'S'
    documento.save(using=using, update_fields=['cfd_certificado','aplicado',])


    serie,folio = split_letranumero(documento.folio)

    rep  = RepositorioCFDI.objects.using(using).create(
        id = -1,
        modalidad_facturacion = 'CFDI',
        version = '3.3',
        uuid = uuid,
        naturaleza = 'E',
        tipo_comprobante = 'I',
        microsip_documento_tipo = 'Factura',
        folio = '%s%s'%(serie,folio),
        fecha = datetime.now(),
        rfc = rfc_receptor,
        taxid = None,
        nombre = nombre_receptor,
        importe = xml_total  ,
        moneda = 'MXN',
        tipo_cambio = 1,
        es_parcialidad = 'N',
        archivo_nombre = '%s_Factura_%s%s_%s.xml'%(rfc_emisor,serie,folio,fecha_formato),
        xml = xml,
        sello_validado = 'M')

    # ll
    uso_folios_fiscales = ConfiguracionFolioFiscalUso.objects.using(using).get(documento= documento_id)
    uso_folios_fiscales.xml = xml
    uso_folios_fiscales.prov_cert = 'CDIGITAL'
    uso_folios_fiscales.fechahora_timbrado = datetime.now().strftime("%Y-%m-%dT%I:%M:%S")
    uso_folios_fiscales.uuid = uuid
    uso_folios_fiscales.documento = documento.id
    uso_folios_fiscales.cfdi = rep.id
    folios_fiscales = first_or_none(ConfiguracionFolioFiscal.objects.using(using).filter(modalidad_facturacion='CFDI'))
    uso_folios_fiscales.folios_fiscales = folios_fiscales

    uso_folios_fiscales.save(using=using,update_fields=['xml','prov_cert', 'fechahora_timbrado', 'uuid', 'documento','cfdi', 'folios_fiscales'])
    management.call_command( 'syncdb', database = using, interactive=False)

    os.remove(ruta_archivo_ini)
    os.remove('%s.sat'%ruta_archivo_ini)
    # os.remove('%s.xml'%ruta_archivo_ini)