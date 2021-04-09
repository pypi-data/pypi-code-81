# PWBus - BottleClient Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Sun Apr 26 22:09:45 -03 2020

import traceback

from pwbus_web.client.client import Client

# BottleClient
#
#


class PwbusBootleClient(Client):

    def setResponseHeaders(self, headers):
        try:
            for key in headers:
                if key in ['Pwbus-Message-Id', 'Pwbus-Correlation-Id', 'Pwbus-Status-Code']:
                    print("pwbus_web.client.PwbusBootleClient - Header: ", key, '=', headers[key])
                    self.response.add_header(key, headers[key])
        except:
            print("Error: pwbus_web.client.PwbusBootleClient.setResponseHeaders")
            traceback.print_exc()
            raise
