from django_microsip_base.libs.models_base.models import Registry, FolioVenta
from microsip_api.apps.cfdi.certificador.core import CertificadorSAT
from microsip_api.apps.cfdi.core import ClavesComercioDigital
import os
from django.conf import settings

class InformacionFacturacion():
    def __init__(self, **kwargs):
        self.datos_facturacion_path = settings.EXTRA_INFO['ruta_datos_facturacion']
        self.rfc = kwargs.get('rfc', None)
        self.passwords = kwargs.get('passwords', self.get_passwords())
        self.password = kwargs.get('password', self.get_password())
        self.errors=[]
    
    def get_passwords(self):
        passwords = ClavesComercioDigital("%s\\comercio_digital_claves.xlsx"%self.datos_facturacion_path)
        if passwords:
            return passwords
        return None

    def get_password(self):
        if self.rfc and self.passwords: 
            try:
                return self.passwords[rfc]
            except KeyError:    
                return None

        return None

    def is_valid(self, **kwargs):
        if self.errors:
            return False
        
        if not self.rfc:
            errors.append("RFC de empresa invalido")
            return False

        if self.passwords.errors:
            self.errors.append(self.passwords.errors) 
            return False
        
        if not self.password: 
            errors.append("No a encontro password de Comercio Digital.")
            
        sellos_path = '%s\\sellos\\'%self.datos_facturacion_path

        try:
            carpetas = os.listdir(sellos_path)
        except WindowsError:
            errors.append("No se encontro carpeta [%s]"%sellos_path)
            return False
        else:
            certificador_sat = CertificadorSAT(self.datos_facturacion_path)
            errors_cert = certificador_sat.certificar(empresa_folder_name= self.rfc)
            if errors_cert:
                self.errors.append(errors_cert)
                return False

        if FolioVenta.objects.filter(tipo_doc = 'F', modalidad_facturacion = 'CFDI').count() == 0:
            self.errors.append("No se a definido el folio automatico para las facturas CFDI")
            return False

        return True