from rs4 import attrdict
import time
import sys
import os
import json
from urllib.parse import urlparse, quote
from .hyper import HTTPConnection

class HttpResponse:
    def __init__ (self, r):
        self.headers = self._rebuild_headers (r.headers)
        self.events = r.events
        self.status_code = r.status
        self.reason =  r.reason
        self.content = r.read ()

    def _rebuild_headers (self, headers):
        headers_ = attrdict.CaseInsensitiveDict ()
        for k, v in headers.items ():
            headers_ [k.decode ()] = v.decode ()
        return headers_

    @property
    def text (self):
        return self.content.decode ()

    def json (self):
        json.loads (self.text)

    def get_pushes (self):
        self.conn.get_pushes ()


class Session:
    def __init__ (self, endpoint):
        self.endpoint = endpoint
        parts = urlparse (self.endpoint)
        self.conn = HTTPConnection(parts.netloc, enable_push = True, secure=parts.scheme == 'https')

    def urlencode (self, params, to_bytes = True):
        fm = []
        for k, v in list(params.items ()):
            fm.append ("%s=%s" % (quote (k), quote (str (v))))
        if to_bytes:
            return "&".join (fm).encode ("utf8")
        return "&".join (fm)

    def _rebuild_header (self, headers_, data):
        headers_ = headers_ or {}
        headers = attrdict.CaseInsensitiveDict ()
        for k, v in headers_.items ():
            headers [k] = v
        if data and headers.get ('content-type') is None:
            headers ['Content-Type'] = 'application/x-www-form-urlencoded'
        return headers

    def _request (self, method, url, data = None, headers = None):
        headers = self._rebuild_header (headers, data)
        if data:
            data = self.urlencode (data)
        self.conn.request (method.upper (), url, data, headers)
        return HttpResponse (self.conn.get_response())

    def get (self, url, headers = {}):
        return self._request ('GET', url, headers = headers)

    def post (self, url, data, headers = {}):
        return self._request ('POST', url, data, headers)
