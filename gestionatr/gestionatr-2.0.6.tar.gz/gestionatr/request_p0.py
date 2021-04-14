from __future__ import absolute_import

aux = {
    'catral': {
        'url': "https://0138.atr.gisce.cloud/Sync?WSDL",
        'user': "0898",
        'password': "12345",
        'file': """
<?xml version='1.0' encoding='UTF-8'?><MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad"><Cabecera><CodigoREEEmpresaEmisora>0898</CodigoREEEmpresaEmisora><CodigoREEEmpresaDestino>0138</CodigoREEEmpresaDestino><CodigoDelProceso>P0</CodigoDelProceso><CodigoDePaso>01</CodigoDePaso><CodigoDeSolicitud>202103312763</CodigoDeSolicitud><SecuencialDeSolicitud>01</SecuencialDeSolicitud><FechaSolicitud>2021-03-31T10:33:57</FechaSolicitud><CUPS>ES0138000000070059LR0F</CUPS></Cabecera><ValidacionCliente><TipoIdentificador>NI</TipoIdentificador><Identificador>29004636A</Identificador></ValidacionCliente></MensajeSolicitudInformacionAlRegistroDePS>
"""
    },
    'prohida': {
        'url': "https://www.ov.prohida.es/Sync?WSDL",
        'user': "0971",
        'password': "12345",
        'file': """<MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad"><Cabecera><CodigoREEEmpresaEmisora>0971</CodigoREEEmpresaEmisora><CodigoREEEmpresaDestino>0310</CodigoREEEmpresaDestino><CodigoDelProceso>P0</CodigoDelProceso><CodigoDePaso>01</CodigoDePaso><CodigoDeSolicitud>202103306059</CodigoDeSolicitud><SecuencialDeSolicitud>01</SecuencialDeSolicitud><FechaSolicitud>2021-03-30T15:04:58</FechaSolicitud><CUPS>ES0310000000133300EC0F</CUPS></Cabecera><ValidacionCliente><TipoIdentificador>NI</TipoIdentificador><Identificador>10074409H</Identificador></ValidacionCliente></MensajeSolicitudInformacionAlRegistroDePS>"""
    },
    'viesgo': {
        'url': "https://viesgop0.app.viesgo.com/syncRequest.wsdl",
        'user': "0762",
        'password': "SOMENE.62",
        'file': """
<MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad">
        <Cabecera>
                <CodigoREEEmpresaEmisora>0762</CodigoREEEmpresaEmisora>
                <CodigoREEEmpresaDestino>0027</CodigoREEEmpresaDestino>
                <CodigoDelProceso>P0</CodigoDelProceso>
                <CodigoDePaso>01</CodigoDePaso>
                <CodigoDeSolicitud>981412111009</CodigoDeSolicitud>
                <SecuencialDeSolicitud>01</SecuencialDeSolicitud>
                <FechaSolicitud>2020-09-09T01:13:37</FechaSolicitud>
                <CUPS>ES0027700035011007SS0F</CUPS>
        </Cabecera>
</MensajeSolicitudInformacionAlRegistroDePS>
        """
    },


    'endesa': {
        'url': "http://trader-eapi.de-c1.eu1.cloudhub.io/api/P0?wsdl",
        'user': "ESGSF076202@sf.es", #"e16732136a5c4a8cadc552717c14fe47",
        'password': "somaltes202007", #"C9e62044f76A4BA1a08D0Ac22421C336",
#         'file': """
# <?xml version='1.0' encoding='UTF-8'?>
# <MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad"><Cabecera><CodigoREEEmpresaEmisora>0432</CodigoREEEmpresaEmisora>
# <CodigoREEEmpresaDestino>0031</CodigoREEEmpresaDestino><CodigoDelProceso>P0</CodigoDelProceso><CodigoDePaso>01</CodigoDePaso>
# <CodigoDeSolicitud>202009101893</CodigoDeSolicitud><SecuencialDeSolicitud>01</SecuencialDeSolicitud><FechaSolicitud>2020-09-10T16:41:06</FechaSolicitud>
# <CUPS>ES0031446384656001NF0F</CUPS></Cabecera><ValidacionCliente><TipoIdentificador>NI</TipoIdentificador><Identificador>G55010961</Identificador></ValidacionCliente>
# </MensajeSolicitudInformacionAlRegistroDePS>
#         """,
        'file': """
<?xml version='1.0' encoding='UTF-8'?>                                                                                                                                                                                 
<MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad"><Cabecera><CodigoREEEmpresaEmisora>0762</CodigoREEEmpresaEmisora>
<CodigoREEEmpresaDestino>0031</CodigoREEEmpresaDestino><CodigoDelProceso>P0</CodigoDelProceso><CodigoDePaso>01</CodigoDePaso>
<CodigoDeSolicitud>202009101893</CodigoDeSolicitud><SecuencialDeSolicitud>01</SecuencialDeSolicitud><FechaSolicitud>2020-09-10T16:41:06</FechaSolicitud>
<CUPS>ES0031405925962008DX0F</CUPS></Cabecera><ValidacionCliente><TipoIdentificador>NI</TipoIdentificador><Identificador>G55010961</Identificador></ValidacionCliente>
</MensajeSolicitudInformacionAlRegistroDePS>
        """
    },

    'binefar': {
        'url': "https://ov.ger.coop/Sync?WSDL",
        'user': "0762",
        'password': "somenergia",
        'file': """
<MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad">
        <Cabecera>
                <CodigoREEEmpresaEmisora>0762</CodigoREEEmpresaEmisora>
                <CodigoREEEmpresaDestino>0291</CodigoREEEmpresaDestino>
                <CodigoDelProceso>P0</CodigoDelProceso>
                <CodigoDePaso>01</CodigoDePaso>
                <CodigoDeSolicitud>222412111009</CodigoDeSolicitud>
                <SecuencialDeSolicitud>01</SecuencialDeSolicitud>
                <FechaSolicitud>2020-09-09T01:13:37</FechaSolicitud>
                <CUPS>ES0291000000000794KT0F</CUPS>
        </Cabecera>
</MensajeSolicitudInformacionAlRegistroDePS>
        """
    },
    'datacenter': {
        'url': "https://switching.datacenter.gl/wsdl",
        'user': "sw_enova_0967",
        'password': "MmZmZjdh",
        'file': """
<MensajeSolicitudInformacionAlRegistroDePS xmlns="http://localhost/elegibilidad">
        <Cabecera>
                <CodigoREEEmpresaEmisora>0967</CodigoREEEmpresaEmisora>
                <CodigoREEEmpresaDestino>0188</CodigoREEEmpresaDestino>
                <CodigoDelProceso>P0</CodigoDelProceso>
                <CodigoDePaso>01</CodigoDePaso>
                <CodigoDeSolicitud>202010303087</CodigoDeSolicitud>
                <SecuencialDeSolicitud>01</SecuencialDeSolicitud>
                <FechaSolicitud>2020-09-09T01:13:37</FechaSolicitud>
                <CUPS>ES0188000006300505QY1F</CUPS>
        </Cabecera>
</MensajeSolicitudInformacionAlRegistroDePS>
        """
    }
}


from gestionatr.cli import request_p0
distri = "catral"
res = request_p0(aux[distri]['url'], aux[distri]['user'], aux[distri]['password'], aux[distri]['file'])
print res
