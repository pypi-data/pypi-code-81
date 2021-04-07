# PWBus - Request Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Sun Apr 26 21:48:20 -03 2020

import sys
import traceback
from json import dumps
import requests

# Request
#
#


class Request():
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
            print("Error: pwbus-http.request.request.getHeaders")
            raise

    def setResponseHeaders(self, headers):
        pass

    def post(self, payload, headers, text_response=True):
        try:
            data = requests.post(
                "http://pwbus-http/pwbus/v1/request",
                data=dumps(payload),
                headers=headers
            )
            resp_headers = dict(data.headers)
            self.setResponseHeaders(resp_headers)
            return {"data": data.json() if text_response else data, "headers": resp_headers}

        except:
            traceback.print_exc()
            print("Error: pwbus_http.request.post")
            raise
