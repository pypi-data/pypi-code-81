# #encoding:utf-8
# from django.db import models
# from django.db import router
# from django.core.cache import cache
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.sessions.models import Session

# from django.core.exceptions import ObjectDoesNotExist
# from microsip_api.comun.sic_db import next_id, first_or_none
# import django.dispatch

# articulo_clave_save_signal = django.dispatch.Signal()
# plazo_condicion_pago_save_signal = django.dispatch.Signal()

# from microsip_api.models_base.comun.articulos import *
# from microsip_api.models_base.comun.catalogos import *
# from microsip_api.models_base.comun.clientes import *
# from microsip_api.models_base.comun.listas import *
# from microsip_api.models_base.comun.otros import *
# from microsip_api.models_base.comun.proveedores import *
# from microsip_api.models_base.comun.cfdi import *

# from microsip_api.models_base.configuracion.folios_fiscales import *
# from microsip_api.models_base.configuracion.preferencias import *

# from microsip_api.models_base.punto_de_venta.documentos import *
# from microsip_api.models_base.punto_de_venta.listas import *

# from microsip_api.models_base.compras.documentos import *
# from microsip_api.models_base.compras.otros import *

# from microsip_api.models_base.cuentas_por_pagar.documentos import *
# from microsip_api.models_base.cuentas_por_pagar.catalogos import *

# from microsip_api.models_base.cuentas_por_cobrar.documentos import *
# from microsip_api.models_base.cuentas_por_cobrar.catalogos import *

# from microsip_api.models_base.ventas.documentos import *

# from microsip_api.models_base.inventarios.documentos import *
# from microsip_api.models_base.inventarios.otros import *
# from microsip_api.models_base.inventarios.catalogos import *

# from microsip_api.models_base.contabilidad.documentos import *
# from microsip_api.models_base.contabilidad.catalogos import *
# from microsip_api.models_base.contabilidad.listas import *

# ################################################################
# ####                                                        ####
# ####                        OTROS                           ####
# ####                                                        ####
# ################################################################
 
# @receiver(post_save)
# def clear_cache(sender, **kwargs):
#     if sender != Session:
#         cache.clear()

# class DatabaseSucursal(models.Model):  
#     name = models.CharField(max_length=100)
#     empresa_conexion = models.CharField(max_length=200)
#     sucursal_conexion = models.CharField(max_length=200)
#     sucursal_conexion_name = models.CharField(max_length=200)
    
#     def __str__(self):  
#           return self.name    
          
#     class Meta:
#         app_label =u'auth'
        
# class ConexionDB(models.Model):  
#     nombre = models.CharField(max_length=100)
#     TIPOS = (('L', 'Local'),('R', 'Remota'),)
#     tipo = models.CharField(max_length=1, choices=TIPOS)
#     servidor = models.CharField(max_length=250)
#     carpeta_datos = models.CharField(max_length=300)
#     usuario = models.CharField(max_length=300)
#     password = models.CharField(max_length=300)

#     def __str__(self):  
#           return self.nombre    
          
#     class Meta:
#         app_label =u'auth' 

# class AplicationPlugin(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)
    
#     def __unicode__(self):
#         return u'%s' % self.nombre

#     class Meta:
#         app_label =u'auth'
#         db_table = u'sic_aplicationplugin'

# ################################################################
# ####                                                        ####
# ####                        CONFIGURACION                   ####
# ####                                                        ####
# ################################################################

# # PREFERENCIAS

# class Registry(RegistryBase):
#     pass

# #FOLIOS FISCALES

# class ConfiguracionFolioFiscal(ConfiguracionFolioFiscalBase): 
#     pass

# class ConfiguracionFolioFiscalUso(ConfiguracionFolioFiscalUsoBase):
#     pass

# ################################################################
# ####                                                        ####
# ####                        COMUN                           ####
# ####                                                        ####
# ################################################################

# # OTROS
    
# class ClaveGeneral(ClaveGeneralBase):
#     pass

# class Pais(PaisBase):
#     def save(self, *args, **kwargs):    
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         super(self.__class__, self).save(*args, **kwargs)
        
#         if self.es_predet == 'S':
#             Pais.objects.using(kwargs['using']).all().exclude(pk=self.id).update(es_predet='N')


# class Estado(EstadoBase):
#     def save(self, *args, **kwargs):
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         super(self.__class__, self).save(*args, **kwargs)
        
#         if self.es_predet == 'S':
#             Estado.objects.using(kwargs['using']).all().exclude(pk=self.id).update(es_predet='N')


# class Ciudad(CiudadBase):
#     def save(self, *args, **kwargs):
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         super(self.__class__, self).save(*args, **kwargs)

#         if self.es_predet == 'S':
#             Ciudad.objects.using(kwargs['using']).all().exclude(pk=self.id).update(es_predet='N')

# class Moneda(MonedaBase):
#     pass

# class TipoCambio(TipoCambioBase):
#     pass

# class ViaEmbarque(ViaEmbarqueBase):
#    pass

# class FolioVenta(FolioVentaBase):
#     pass

# class FolioCompra(FolioCompraBase):
#     pass

# class Atributo(AtributoBase):
#     pass

# class AtributoLista(AtributoListaBase):
#     pass

# # ARTICULOS

# class GrupoLineas(GrupoLineasBase):
#     pass

# class LineaArticulos(LineaArticulosBase):
#     pass

# class Articulo(ArticuloBase):
#     pass

# class ArticuloClaveRol(ArticuloClaveRolBase):
#     pass

# class ArticuloClave(ArticuloClaveBase):
#     def save_send_signal(self, *args, **kwargs):
#         articulo_clave_save_signal.send(sender=self, *args, **kwargs)

# class ArticuloPrecio(ArticuloPrecioBase):
#     pass

# class Almacen(AlmacenBase):
#     pass

# class PrecioEmpresa(PrecioEmpresaBase):
#     pass

# class ArticuloDiscreto(ArticuloDiscretoBase):
#     pass

# class ArticuloDiscretoExistencia(ArticuloDiscretoExistenciaBase):
#     pass

# class ArticuloNivel(ArticuloNivelBase):
#     pass

# #CATALOGOS

# class Banco(BancoBase):
#     pass

# # LISTAS

# class ImpuestoTipo(ImpuestoTipoBase):
#     pass

# class Impuesto(ImpuestoBase):
#     def save(self, *args, **kwargs):    
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         super(self.__class__, self).save(*args, **kwargs)

#         if self.es_predet == 'S':
#             Impuesto.objects.using(kwargs['using']).all().exclude(pk=self.id).update(es_predet='N')


# class ImpuestosArticulo(ImpuestoArticuloBase):
#     pass

# class Vendedor(VendedorBase):
#     pass


# # CLIENTES

# class ClienteTipo(ClienteTipoBase):
#     pass

# class CondicionPago(CondicionPagoBase):
#     def save(self, *args, **kwargs):    
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         super(self.__class__, self).save(*args, **kwargs)

#         if self.es_predet == 'S':
#             CondicionPago.objects.using(kwargs['using']).all().exclude(pk=self.id).update(es_predet='N')


# class CondicionPagoPlazo(CondicionPagoPlazoBase):
#     def save_send_signal(self, *args, **kwargs):
#         articulo_clave_save_signal.send(sender=self, *args, **kwargs)

# class Cliente(ClienteBase):
#     pass

# class Zona(ZonaBase):
#     pass

# class ClienteClaveRol(ClienteClaveRolBase):
#     pass

# class ClienteClave(ClienteClaveBase):
#     pass

# class ClienteDireccion(ClienteDireccionBase):
#     pass

# class LibresClientes(LibreClienteBase):
#     pass
    
# # PROVEEDORES

# class ProveedorTipo(ProveedorTipoBase):
#     pass
        
# class Proveedor(ProveedorBase):
#     pass

# ################################################################
# ####                                                        ####
# ####                      COMPRAS                           ####
# ####                                                        ####
# ################################################################

# # OTROS

# class Aduana(AduanaBase):
#     pass

# class Pedimento(PedimentoBase):
#     pass

# class DesglosePedimento(DesglosePedimentoBase):
#     pass

# class PedimentoCapa(PedimentoCapaBase):
#     pass

# class PedimentoCapaUso(PedimentoCapaUsoBase):
#     pass

# # DOCUMENTOS

# class ComprasConsignatario(ComprasConsignatarioBase):
#     pass

# class ComprasDocumento(ComprasDocumentoBase):
#     def next_folio( self, connection_name=None, **kwargs ):
#         ''' Funcion para generar el siguiente folio de un documento de ventas '''

#         #Parametros opcionales
#         serie = kwargs.get('serie', None)
#         consecutivos_folios = FolioCompra.objects.using(connection_name).filter(tipo_doc = self.tipo)
#         if serie:
#             consecutivos_folios = consecutivos_folios.filter(serie=serie)

#         consecutivo_row = first_or_none(consecutivos_folios)
#         consecutivo = ''
#         if consecutivo_row:
#             consecutivo = consecutivo_row.consecutivo 
#             serie = consecutivo_row.serie
#             if serie == u'@':
#                 serie = ''
                
#         folio = '%s%s'% (serie,("%09d" % int(consecutivo))[len(serie):]) 

#         consecutivo_row.consecutivo = consecutivo_row.consecutivo + 1
#         consecutivo_row.save()

#         return folio

#     def save(self, *args, **kwargs):
#         if self.folio == '':
#             kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#             self.folio = self.next_folio(connection_name=kwargs['using'])

#         super(self.__class__, self).save(*args, **kwargs)

# class ComprasDocumentoCargoVencimiento(ComprasDocumentoCargoVencimientoBase):
#     pass

# class ComprasDocumentoDetalle(ComprasDocumentoDetalleBase):
#     pass

# class ComprasDocumentoImpuesto(ComprasDocumentoImpuestoBase):
#     pass

# class ComprasDocumentoLiga(ComprasDocumentoLigaBase):
#     pass

# class ComprasDocumentoLigaDetalle(ComprasDocumentoLigaDetalleBase):
#     pass


# #####################################################
# ##
# ##                         INVENTARIOS
# ##
# ##
# #####################################################

# # CATALOGOS

# class InventariosConcepto(InventariosConceptoBase):
#     pass

# class InventariosCentroCostos(InventariosCentroCostosBase):
#     pass

# #  DOCUMENTOS

# class InventariosDocumento(InventariosDocumentoBase):

#     def next_folio( self, connection_name=None):
#         ''' Funcion para generar el siguiente folio de un documento inventario '''

#         folio = ''
#         concepto_in = self.concepto
#         if concepto_in.folio_autom and concepto_in.sig_folio:
#             folio = "%09d" % int(concepto_in.sig_folio)
#         concepto_in.sig_folio = "%09d" % (int(concepto_in.sig_folio)+1)
#         concepto_in.save()

#         return folio

#     def save(self, *args, **kwargs):
#         if not self.folio and self.concepto.folio_autom == 'S':
#             kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#             self.folio = self.next_folio()

#         super(self.__class__, self).save(*args, **kwargs)

# class InventariosDocumentoDetalle(InventariosDocumentoDetalleBase):
#     pass

# class InventariosDocumentoIF(InventariosDocumentoIFBase):
#     pass

# class InventariosDocumentoIFDetalle(InventariosDocumentoIFDetalleBase):
#     pass

# # OTROS

# class InventariosDesgloseEnDiscretos(InventariosDesgloseEnDiscretosBase):
#     pass

# class InventariosDesgloseEnDiscretosIF(InventariosDesgloseEnDiscretosIFBase):
#     pass


# ################################################################
# ####                                                        ####
# ####               MODELOS CUENTAS POR PAGAR                ####
# ####                                                        ####
# ################################################################

# # CATALOGOS

# class CuentasXPagarConcepto(CuentasXPagarConceptoBase):
#     pass

# class CuentasXPagarCondicionPago(CuentasXPagarCondicionPagoBase):
#     pass

# class CuentasXPagarCondicionPagoPlazoBase(CuentasXPagarCondicionPagoPlazoBase):
#     pass

# # DOCUMENTOS

# class CuentasXPagarDocumento(CuentasXPagarDocumentoBase):
#     pass
# class CuentasXPagarDocumentoImportes(CuentasXPagarDocumentoImportesBase):
#    pass

# class CuentasXPagarDocumentoImportesImpuesto(CuentasXPagarDocumentoImportesImpuestoBase):
#     pass

# class CuentasXPagarDocumentoCargoLibres(CuentasXPagarDocumentoCargoLibresBase):
#     pass

# ################################################################
# ####                                                        ####
# ####               MODELOS CUENTAS POR COBRAR               ####
# ####                                                        ####
# ################################################################

# # CATALOGOS

# class CuentasXCobrarConcepto(CuentasXCobrarConceptoBase):
#     pass

# # DOCUMENTOS

# class CuentasXCobrarDocumento(CuentasXCobrarDocumentoBase):
#     pass

# class CuentasXCobrarDocumentoImportes(CuentasXCobrarDocumentoImportesBase):
#     pass

# class CuentasXCobrarDocumentoImportesImpuesto(CuentasXCobrarDocumentoImportesImpuestoBase): 
#     pass
    
# class CuentasXCobrarDocumentoCargoVencimiento(CuentasXCobrarDocumentoCargoVencimientoBase):
#     pass

# class CuentasXCobrarDocumentoCargoLibres(CuentasXCobrarDocumentoCargoLibresBase):
#     pass

# class CuentasXCobrarDocumentoCreditoLibres(CuentasXCobrarDocumentoCreditoLibresBase):
#     pass

# ################################################################
# ####                                                        ####
# ####               MODELOS CONTABILIDAD                     ####
# ####                                                        ####
# ################################################################

# # CATALOGOS

# class ContabilidadCuentaContable(ContabilidadCuentaContableBase):
#     pass

# # DOCUMENTOS

# class ContabilidadGrupoPolizaPeriodo(ContabilidadGrupoPolizaPeriodoBase):
#     pass

# class ContabilidadRecordatorio(ContabilidadRecordatorioBase):
#     pass

# class ContabilidadDocumento(ContabilidadDocumentoBase):
#     def next_folio( self, using=None):
#         """ Generar un folio nuevo de una poliza e incrementa el consecutivo de folios """
#         tipo_poliza = self.tipo_poliza
#         prefijo = tipo_poliza.prefijo
#         if not prefijo:
#             prefijo = ''
#         tipo_consecutivo = tipo_poliza.tipo_consec

#         try:
#             if tipo_consecutivo == 'M':
#                 tipo_poliza_det = TipoPolizaDetalle.objects.get(tipo_poliza = tipo_poliza, mes= self.fecha.month, ano = self.fecha.year)
#             elif tipo_consecutivo == 'E':
#                 tipo_poliza_det = TipoPolizaDetalle.objects.get(tipo_poliza = tipo_poliza, ano=self.fecha.year, mes=0)
#             elif tipo_consecutivo == 'P':
#                 tipo_poliza_det = TipoPolizaDetalle.objects.get(tipo_poliza = tipo_poliza, mes=0, ano =0)
#         except ObjectDoesNotExist:
#             if tipo_consecutivo == 'M':      
#                 tipo_poliza_det = TipoPolizaDetalle.objects.create(id=next_id('ID_CATALOGOS', using), tipo_poliza=tipo_poliza, ano=self.fecha.year, mes=self.fecha.month, consecutivo = 1,)
#             elif tipo_consecutivo == 'E':
#                 #Si existe permanente toma su consecutivo para crear uno nuevo si no existe inicia en 1
#                 consecutivo = TipoPolizaDetalle.objects.filter(tipo_poliza = tipo_poliza, mes=0, ano =0).aggregate(max = Sum('consecutivo'))['max']

#                 if consecutivo == None:
#                     consecutivo = 1

#                 tipo_poliza_det = TipoPolizaDetalle.objects.create(id=next_id('ID_CATALOGOS', using), tipo_poliza=tipo_poliza, ano= self.fecha.year, mes=0, consecutivo=consecutivo,)
#             elif tipo_consecutivo == 'P':
#                 consecutivo = TipoPolizaDetalle.objects.all().aggregate(max = Sum('consecutivo'))['max']

#                 if consecutivo == None:
#                     consecutivo = 1

#                 tipo_poliza_det = TipoPolizaDetalle.objects.create(id=next_id('ID_CATALOGOS', using), tipo_poliza=tipo_poliza, ano=0, mes=0, consecutivo = consecutivo,)                                
        
#         folio = '%s%s'% (prefijo,("%09d" % tipo_poliza_det.consecutivo)[len(prefijo):]) 

#         #CONSECUTIVO DE FOLIO DE POLIZA
#         tipo_poliza_det.consecutivo += 1 
#         tipo_poliza_det.save()
        
#         return folio
    
#     def save(self, *args, **kwargs):
        
#         if not self.poliza:
#             kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#             self.poliza = self.next_folio(using=kwargs['using'])

#         super(self.__class__, self).save(*args, **kwargs)
   

# class ContabilidadDocumentoDetalle(ContabilidadDocumentoDetalleBase):
#     pass

# # LISTAS

# class TipoPoliza(TipoPolizaBase):
#     pass

# class TipoPolizaDetalle(TipoPolizaDetalleBase):
#     pass

# class ContabilidadDepartamento(ContabilidadDepartamentoBase):
#     pass

# ################################################################
# ####                                                        ####
# ####                    MODELOS VENTAS                      ####
# ####                                                        ####
# ################################################################

# # DOCUMENTOS
# class VentasDocumento(VentasDocumentoBase):
#     def next_folio( self, connection_name=None, **kwargs ):
#         ''' Funcion para generar el siguiente folio de un documento de ventas '''

#         #Parametros opcionales
#         serie = kwargs.get('serie', None)
#         consecutivos_folios = FolioVenta.objects.using(connection_name).filter(tipo_doc = self.tipo, modalidad_facturacion = self.modalidad_facturacion)
#         if serie:
#             consecutivos_folios = consecutivos_folios.filter(serie=serie)

#         consecutivo_row = first_or_none(consecutivos_folios)
#         consecutivo = ''
#         if consecutivo_row:
#             consecutivo = consecutivo_row.consecutivo 
#             serie = consecutivo_row.serie
#             if serie == u'@':
#                 serie = ''

#         folio = '%s%s'% (serie,("%09d" % int(consecutivo))[len(serie):]) 

#         consecutivo_row.consecutivo = consecutivo_row.consecutivo + 1
#         consecutivo_row.save(using=connection_name)
#         return folio, consecutivo


#     def save(self, *args, **kwargs):
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
#         consecutivo = ''
#         #Si no se define folio se asigna uno
#         if self.folio == '':
#             self.folio, consecutivo = self.next_folio(connection_name=kwargs['using'])

#         super(self.__class__, self).save(*args, **kwargs)
        
#         #si es factura 
#         if consecutivo != '' and self.tipo == 'F' and self.modalidad_facturacion == 'CFDI':
#             folios_fiscales = first_or_none(ConfiguracionFolioFiscal.objects.using(kwargs['using']).filter(modalidad_facturacion=self.modalidad_facturacion))
#             if not folios_fiscales:
#                 ConfiguracionFolioFiscal.objects.using(kwargs['using']).create(
#                         serie = '@',
#                         folio_ini = 1,
#                         folio_fin = 999999999,
#                         ultimo_utilizado = 0,
#                         num_aprobacion ="1",
#                         ano_aprobacion = 1,
#                         modalidad_facturacion = self.modalidad_facturacion,
#                     )
#                 folios_fiscales = first_or_none(ConfiguracionFolioFiscal.objects.using(kwargs['using']).filter(modalidad_facturacion=self.modalidad_facturacion))
        

#             if folios_fiscales:
#                 ConfiguracionFolioFiscalUso.objects.using(kwargs['using']).create(
#                         id= -1,
#                         folios_fiscales = folios_fiscales,
#                         folio= consecutivo,
#                         fecha = datetime.now(),
#                         sistema = self.sistema_origen,
#                         documento = self.id,
#                         xml = '',
#                     )


# class VentasDocumentoVencimiento(VentasDocumentoVencimientoBase):
#     pass

# class VentasDocumentoImpuesto(VentasDocumentoImpuestoBase):
#     pass


# class VentasDocumentoDetalle(VentasDocumentoDetalleBase):
#     pass

# class VentasDocumentoLiga(VentasDocumentoLigaBase):
#     pass

# class VentasDocumentoFacturaLibres(VentasDocumentoFacturaLibresBase):
#     pass
    
# class VentasDocumentoFacturaDevLibres(VentasDocumentoFacturaDevLibresBase):
#     pass

# ################################################################
# ####                                                        ####
# ####                MODELOS PUNTO DE VENTAS                 ####
# ####                                                        ####
# ################################################################

# #LISTAS
# class FormaCobro(FormaCobroBase):
#     pass

# class FormaCobroReferencia(FormaCobroReferenciaBase):
#     pass

# class Cajero(CajeroBase):
#     pass

# class Caja(CajaBase):
#     pass 

# class CajaFolios(CajaFoliosBase):
#     pass 
    
# class CajeroCaja(CajeroCajaBase):
#     pass

# class CajaMovimiento(CajaMovimientoBase):
#     pass

# class CajaMovimientoFondo(CajaMovimientoFondoBase):
#     pass

# #DOCUMENTOS

# class PuntoVentaDocumento(PuntoVentaDocumentoBase): 
#     def next_folio( self, connection_name=None, **kwargs ):
#         ''' Funcion para generar el siguiente folio de un documento de ventas '''

#         #Parametros opcionales
#         serie = kwargs.get('serie', None)
#         consecutivos_folios = FolioVenta.objects.using(connection_name).filter(tipo_doc = self.tipo, modalidad_facturacion = self.modalidad_facturacion)
#         if serie:
#             consecutivos_folios = consecutivos_folios.filter(serie=serie)

#         consecutivo_row = first_or_none(consecutivos_folios)
#         consecutivo = ''
#         if consecutivo_row:
#             consecutivo = consecutivo_row.consecutivo 
#             serie = consecutivo_row.serie
#             if serie == u'@':
#                 serie = ''

#         folio = '%s%s'% (serie,("%09d" % int(consecutivo))[len(serie):]) 

#         consecutivo_row.consecutivo = consecutivo_row.consecutivo + 1
#         consecutivo_row.save()

#         return folio, consecutivo - 1

#     def save(self, *args, **kwargs):
#         kwargs['using'] = kwargs.get('using', router.db_for_write(self.__class__, instance=self))
        
#         consecutivo = ''
#         #Si no se define folio se asigna uno
#         if self.folio == '':
#             self.folio, consecutivo = self.next_folio(connection_name=kwargs['using'])
#         super(self.__class__, self).save(*args, **kwargs)
        
#         #si es factura 
#         if consecutivo != '' and self.tipo == 'F' and self.modalidad_facturacion == 'CFDI':
#             folios_fiscales = first_or_none(ConfiguracionFolioFiscal.objects.filter(modalidad_facturacion=self.modalidad_facturacion))
#             if folios_fiscales:
#                 ConfiguracionFolioFiscalUso.objects.create(
#                         id= -1,
#                         folios_fiscales = folios_fiscales,
#                         folio= consecutivo,
#                         fecha = datetime.now(),
#                         sistema = self.sistema_origen,
#                         documento = self.id,
#                         xml = '',
#                     )


# class PuntoVentaDocumentoDetalle(PuntoVentaDocumentoDetalleBase):
#     pass

# class PuntoVentaDocumentoLiga(PuntoVentaDocumentoLigaBase):
#    pass

# class PuntoVentaDocumentoLigaDetalle(PuntoVentaDocumentoLigaDetalleBase):
#     pass

# class PuntoVentaDocumentoDetalleTransferencia(PuntoVentaDocumentoDetalleTransferenciaBase):
#     pass

# class PuntoVentaCobro(PuntoVentaCobroBase):
#     pass

# class PuntoVentaCobroReferencia(PuntoVentaCobroReferenciaBase):
#     pass

# class PuntoVentaDocumentoImpuesto(PuntoVentaDocumentoImpuestoBase):
#     pass

# class PuntoVentaDocumentoImpuestoGravado(PuntoVentaDocumentoImpuestoGravadoBase):
#     pass

# ################################################################
# ####                                                        ####
# ####                        NOMINA                          ####
# ####                                                        ####
# ################################################################

# from microsip_api.models_base.nomina.catalogos import *
# from microsip_api.models_base.nomina.listas import *
# from microsip_api.models_base.nomina.movimientos import *
# from microsip_api.models_base.nomina.nominas import *

# #Catalogos
# class NominaEmpleado(NominaEmpleadoBase):
#     pass

# class NominaFrecuenciaPago(NominaFrecuenciaPagoBase):
#     pass

# class NominaConcepto(NominaConceptoBase):
#     pass

# #listas
# class NominaTablaTipo(NominaTablaTipoBase):
#     pass

# class NominaTabla(NominaTablaBase):
#     pass

# #movimientos
# class NominaPrestamo(NominaPrestamoBase):
#     pass

# #Nominas
# class NominaNomina(NominaNominaBase):
#     pass

# class NominaNominaPago(NominaNominaPagoBase):
#     pass

# class NominaNominaPagoDetalle(NominaNominaPagoDetalleBase):
#     pass


# # CFDI#######
# class RepositorioCFDI(RepositorioCFDIBase):
#     pass