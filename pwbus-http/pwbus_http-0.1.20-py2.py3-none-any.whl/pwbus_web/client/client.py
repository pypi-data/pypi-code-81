# PWBus - Client Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Sun Apr 26 21:48:20 -03 2020

import sys
import traceback
from json import dumps
import requests

# BootleClient
#
#


class Client():
    def __init__(self, request, response, channel, task_id):
        self.request = request
        self.response = response
        self.channel = channel
        self.task_id = task_id
        self.headers = request.headers
        self.retry = False

    def isRetry(self):
        return self.retry

    def getHeaders(self):
        try:
            if 'pwbus-correlation-id' in self.headers or \
                    'Pwbus-Correlation-Id' in self.headers:
                headers = {
                    "Content-Type": "application/json",
                    "Pwbus-Channel": self.channel,
                    "pwbus-correlation-id": self.headers[
                        'pwbus-correlation-id'
                        if 'pwbus-correlation-id' in self.headers
                        else 'Pwbus-Correlation-Id'
                    ]
                }

                self.retry = True
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Pwbus-Channel": self.channel,
                    "Pwbus-Task-Id": self.task_id
                }
            return headers

        except:
            traceback.print_exc()
            print("Error: pwbus_web.client.Client.getHeaders")
            raise

    def setResponseHeaders(self, headers):
        pass

    def post(self, payload, headers):
        try:
            data = requests.post(
                "http://pwbus-web/pwbus/v1/request",
                data=dumps(payload),
                headers=headers
            )
            resp_headers = dict(data.headers)
            self.setResponseHeaders(resp_headers)
            print("retornou")
            return {"data": data.text, "headers": resp_headers}

        except:
            traceback.print_exc()
            print("Error: pwbus_web.client.Client.post")
            raise
