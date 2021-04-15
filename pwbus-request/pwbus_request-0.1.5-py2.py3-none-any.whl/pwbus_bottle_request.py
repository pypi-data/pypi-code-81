# PWBus - PwbusBootleRequest Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Sun Apr 26 22:09:45 -03 2020

import sys

from pwbus_request.request import Request

# PwbusBootleRequest
#
#


class PwbusBootleRequest(Request):

    def setResponseHeaders(self, headers):
        try:
            for key in headers:
                if key in ['Pwbus-Message-Id', 'Pwbus-Correlation-Id', 'Pwbus-Status-Code']:
                    self.response.add_header(key, headers[key])
        except:
            print(
                f'Error: pwbus_request.PwbusBootleRequest.setResponseHeaders - Message {sys.exc_info()[-1]}')
            raise
