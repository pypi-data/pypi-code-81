#encoding:utf-8
from django_microsip_base.libs.models_base.models import Moneda, VentasDocumento, CondicionPagoPlazo, Cliente, ClienteDireccion
from django.db import connections, router
from django.db.models import Sum
from decimal import Decimal
from datetime import date, timedelta
from microsip_api.comun.comun_functions import get_short_folio
from microsip_api.comun.sic_db import first_or_none
import re


class CargosClientes(list):
    '''Obtener los cargos de los clientes indicados
    si es nesesario regresa remisiones tambien.
     '''

    def __init__(self, validar, **kwargs):
        CLIENTES_IDS = tuple(kwargs.get('clientes_ids', []))
        monto_minimo_mn = kwargs.get('monto_minimo_mn', 0)
        tomar_remisiones = kwargs.get('tomar_remisiones', False)
        validar_telefono = False
        validar_correo = False

        self.validar = validar
        if validar == 'email':
            validar_correo = True
        elif validar == 'sms':
            validar_telefono = True

        self.clientes_cargos = {}
        self.clientes_informacion_invalida = []
        self.tomar_remisiones = tomar_remisiones
        self.using = router.db_for_write(Moneda)
        self.validar_correo = validar_correo
        self.validar_telefono = validar_telefono
        self.montos_minimos = {}
        self.tipos_cambio = {}
        self.monedas = {}
        # para sacar las monedas en un diccionario
        monedas_list = Moneda.objects.all().values('id', 'simbolo')
        for moneda in monedas_list:
            self.monedas[moneda['id']] = moneda['simbolo']
            tipo_cambio = self.get_tipo_cambio(moneda['id'])
            self.tipos_cambio[moneda['id']] = tipo_cambio
            self.montos_minimos[moneda['id']] = Decimal(monto_minimo_mn) / tipo_cambio

        if CLIENTES_IDS:
            self.clientes_sin_mensaje = kwargs.get('clientes_ids')
        else:
            self.clientes_sin_mensaje = []

        self.get_mensajes_data(CLIENTES_IDS)

    def get_tipo_cambio(self, moneda_id):
        c = connections[self.using].cursor()
        c.execute('SELECT * FROM GET_TIPO_CAMBIO_S({moneda_id}, CURRENT_DATE)'.format(**{'moneda_id': moneda_id, }))
        tipo_cambio = c.fetchall()[0][2]
        c.close()
        return tipo_cambio

    def cargos_de_clientes(self, clientes_ids=None):

        condicion_clientes = ''
        if clientes_ids:
            numero_ids = len(clientes_ids)
            clientes_ids = map(str, clientes_ids)
            clientes_ids = ','.join(clientes_ids)
            condicion_clientes = 'and a.cliente_id in({}) '.format(clientes_ids)
            if numero_ids == 1:
                condicion_clientes = 'and a.cliente_id ={} '.format(clientes_ids)

        condicion_datos_cliente = ''
        if self.validar_correo:
            condicion_datos_cliente += 'AND (A.SIC_MAIL_NOENVIAR=0 OR A.SIC_MAIL_NOENVIAR IS NULL) '
        if self.validar == 'sms':
            condicion_datos_cliente += 'AND (A.SIC_SMS_NOENVIAR=0 OR A.SIC_SMS_NOENVIAR IS NULL) '

        args = {
            'condicion_clientes': condicion_clientes,
            'condicion_datos_cliente': condicion_datos_cliente,
        }
        c = connections[self.using].cursor()
        query = '''SELECT DC.EMAIL, DC.TELEFONO1, B.FOLIO,B.SALDO_CARGO,B.SALDO_CLIENTE,A.NOMBRE,A.CLIENTE_ID, B.FECHA_VENCIMIENTO, B.NOMBRE_ABREV_CONCEPTO, B.MONEDA_ID, B.FECHA
            FROM CLIENTES A INNER JOIN DIRS_CLIENTES DC
            ON A.CLIENTE_ID=DC.CLIENTE_ID
            RIGHT JOIN GET_CARGOS_CC(CURRENT_DATE, 'P', '0' ,'S', 'S', 'N') B
            ON B.CLIENTE_ID = A.CLIENTE_ID
            WHERE DC.ES_DIR_PPAL = 'S' {condicion_clientes} {condicion_datos_cliente}
            ORDER BY A.CLIENTE_ID, B.FECHA_VENCIMIENTO'''.format(**args)
        c.execute(query)
        registros = c.fetchall()
        c.close()
        return registros

    def get_remisiones_cliente(self, cliente):
        """ Obtiene remisiones pendientes del cliente indicado. """
        
        total = 0
        data = {
            'total': total,
            'documentos': [],
        }

        remisiones_pendientes = VentasDocumento.objects.filter(tipo='R', estado='P', cliente=cliente).order_by('fecha',)

        for documento in remisiones_pendientes:
            importe_bruto = (documento.importe_neto + documento.otros_cargos + documento.impuestos_total + documento.retenciones_total) 

            if cliente.moneda.es_moneda_local == 'S':
                if not documento.moneda == cliente.moneda:
                    importe_bruto = (documento.importe_neto + documento.otros_cargos + documento.impuestos_total + documento.retenciones_total) * self.tipos_cambio[documento.moneda.id]
                else:
                    importe_bruto = (documento.importe_neto + documento.otros_cargos + documento.impuestos_total + documento.retenciones_total)
                
            else:
                if not documento.moneda == cliente.moneda:
                    importe_bruto = (documento.importe_neto + documento.otros_cargos + documento.impuestos_total + documento.retenciones_total) / self.tipos_cambio[cliente.moneda.id]
                else:
                    importe_bruto = (documento.importe_neto + documento.otros_cargos + documento.impuestos_total + documento.retenciones_total)
                            
            dias = CondicionPagoPlazo.objects.filter(condicion_de_pago=documento.condicion_pago).aggregate(total_dias=Sum('dias'))['total_dias'] or 0 
            #si la condicion de pago no es contado
            if dias > 0:

                vencimiento_fecha = documento.fecha + timedelta(days=dias)
                documento_vencido = vencimiento_fecha < date.today()
                total += importe_bruto
                data['documentos'].append({
                    'concepto': 'Remision',
                    'folio': get_short_folio(documento.folio),
                    'saldo_cargo': '${:,.2f}'.format(importe_bruto),
                    'vencimiento': vencimiento_fecha.strftime("%d/%m/%Y"),
                    'factura_vencida': documento_vencido,
                })
        data['numero_documentos'] = len(data['documentos'])
        data['total'] = total
        return data

    def telefono_valido(self, telefono):
        print(telefono)
        if telefono:
            telefono = telefono.encode('utf-8')
            telefono = re.sub("[^0-9]", "", str(telefono))
            print(telefono)
            print(len(telefono))
            if len(telefono) == 10:
                return True
        return False

    def validar_informacion_envio(self, telefono, email, cliente_nombre):
        """ Validacion de correo y telefono si se indico en la funcion que desea validarse
        Si la informacion es invalida se agrega a clientes con informacion invalida.
        """
        is_valid = True
        if self.validar_telefono and self.telefono_valido(telefono) is False:
            is_valid = False
        if self.validar_correo and email is None:
            is_valid = False

        if not is_valid:
            # Si el cliente no esta ya agregado a los clientes con informacion invalida
            if cliente_nombre not in self.clientes_informacion_invalida:
                self.clientes_informacion_invalida.append(cliente_nombre)

        return is_valid

    def get_cargos_cuentasxcobrar(self, clientes_ids):
        """ Forma un dicionario de los cargos cuentas por cobrar para leer la informacion mas facil. """
        registros = self.cargos_de_clientes(clientes_ids)
        clientes_cargos = {}
        print(registros)
        ''' Checar informacion de todos los cargos '''
        for registro in registros:
            # Mapeamos informacion de cada registro
            print(registro)
            total = registro[4]
            cliente_id = registro[6]
            cliente = Cliente.objects.get(pk=cliente_id)
            cliente_nombre = cliente.nombre.lstrip().rstrip()
            email = registro[0]
            telefono = registro[1]
            vencimiento_fecha = registro[7]
            factura_vencida = vencimiento_fecha < date.today()
            documento_cargo = {
                'concepto': registro[8],
                'folio': get_short_folio(registro[2]),
                'saldo_cargo': '${:,.2f}'.format(registro[3]),
                'vencimiento': vencimiento_fecha.strftime("%d/%m/%Y"),
                'factura_vencida': factura_vencida,
            }

            if self.validar_informacion_envio(telefono=telefono, email=email, cliente_nombre=cliente_nombre):

                # Si el correo no esta en los detalles de mensajes
                if not cliente_id in clientes_cargos:
                    # Inicioalizamo el diccionario
                    clientes_cargos[cliente_id] = {
                        'total': total,
                        'documentos': [],
                        'email': email,
                        'telefono': telefono,
                        'moneda_nombre': cliente.moneda.nombre,
                        'moneda_simbolo': cliente.moneda.simbolo,
                        'moneda_id': cliente.moneda.id,
                    }

                    # indicamos que este cliente si tiene mensaje
                    if str(cliente_id) in self.clientes_sin_mensaje:
                        self.clientes_sin_mensaje.remove(str(cliente_id))
                    numero_documentos = 1
                else:
                    numero_documentos += 1

                clientes_cargos[cliente_id]['documentos'].append(documento_cargo)
                clientes_cargos[cliente_id]['numero_documentos'] = numero_documentos
        return clientes_cargos

    def get_cargos_all(self, ids_clientes):
        clientes_cargos = self.get_cargos_cuentasxcobrar(ids_clientes)
        if self.tomar_remisiones:
            clientes_con_remisiones = VentasDocumento.objects.filter(tipo='R', estado='P').values('cliente').distinct()
            if ids_clientes:
                clientes_con_remisiones = clientes_con_remisiones.filter(cliente__id__in=ids_clientes)
            clientes_con_remisiones = clientes_con_remisiones.values_list('cliente__id', flat=True)
            for cliente_con_remisiones in clientes_con_remisiones:
                cliente = Cliente.objects.get(pk=cliente_con_remisiones)
                direccion = first_or_none(ClienteDireccion.objects.filter(es_ppal='S', cliente=cliente))
                email = ''
                telefono = ''
                if direccion:
                    email = direccion.email
                    telefono = direccion.telefono1
                agregar = True
                if self.validar_correo:
                    if cliente.no_enviar_mail:
                        agregar = False
                if self.validar_telefono:
                    if cliente.no_enviar_sms:
                        agregar = False

                if self.validar_informacion_envio(telefono=telefono, email=email, cliente_nombre=cliente.nombre) and agregar:
                    remisiones_data = self.get_remisiones_cliente(cliente)
                    if cliente_con_remisiones in clientes_cargos:
                        clientes_cargos[cliente_con_remisiones]['total'] += remisiones_data['total']
                        clientes_cargos[cliente_con_remisiones]['documentos'] += remisiones_data['documentos']
                        clientes_cargos[cliente_con_remisiones]['numero_documentos'] += remisiones_data['numero_documentos']

                    else:
                        clientes_cargos[cliente_con_remisiones] = {
                            'total': remisiones_data['total'],
                            'documentos': remisiones_data['documentos'],
                            'email': email,
                            'telefono': telefono,
                            'moneda_nombre': cliente.moneda.nombre,
                            'moneda_simbolo': cliente.moneda.simbolo,
                            'moneda_id': cliente.moneda.id,
                            'numero_documentos': remisiones_data['numero_documentos'],
                        }
        return clientes_cargos

    def get_mensajes_data(self, clientes_ids):
        clientes_cargos = self.get_cargos_all(clientes_ids)
        for cliente_id, cliente in clientes_cargos.items():
            #Si son mas de 50 mensajes no se envian los documentos
            monto_minimo_moneda_cliente = self.montos_minimos[cliente['moneda_id']]
            # Si el total del cliente es 0 no enviar nada
            if cliente['total'] >= monto_minimo_moneda_cliente and cliente['total'] != 0:
                if cliente['numero_documentos'] > 50:
                    cliente['documentos'] = []
                self.append({
                    'email': cliente['email'],
                    'telefono': cliente['telefono'],
                    'documentos_numero': cliente['numero_documentos'],
                    'documentos': cliente['documentos'],
                    'total': '$ {:,.2f}'.format(cliente['total']),
                    'cliente_moneda': cliente['moneda_nombre'],
                    'cliente_moneda_simbolo': cliente['moneda_simbolo'],
                    'cliente_id': cliente_id,
                })

    def get_clientes_sin_mensajes(self):
        clientes = Cliente.objects.filter(id__in=self.clientes_sin_mensaje).values_list('nombre', flat=True)
        return clientes
