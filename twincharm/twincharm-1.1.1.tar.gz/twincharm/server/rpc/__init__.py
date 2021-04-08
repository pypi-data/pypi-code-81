import re
import socket
import locale
from twincharm.response import Response
class TwincharmError(Exception):pass
class BadRequestError(TwincharmError):pass
class InvalidFunctionError(TwincharmError):pass
class Server:
    def __init__(self,address):
        self.addr=address
        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind(address)
        self.funs={}
    def __getattr__(self,attrname):
        if attrname not in self.funs:
            raise AttributeError
        return self.funs[attrname]
    def function(self,fun):
        self.funs[fun.__name__]=fun
        return fun
    def run(self,debug=False):
        print(f'listening on {self.addr}')
        while True:
            m,addr=self.s.recvfrom(1024)
            fun=None
            for f in self.funs:
                if m.startswith(f.encode(locale.getpreferredencoding())):
                    fun=self.funs[f]
            if fun is None:
                self.s.sendto(b'ERR:FHU',addr)
                if debug:
                    raise BadRequestError(f'function header in request {repr(m)} is undefined')
            out=m.decode('utf-8').split(':')[1] 
            resp=fun(out,addr)
            if not (isinstance(resp,bytes)or isinstance(resp,Response)):
                raise InvalidFunctionError(f'function should return type bytes or twincharm.response.Response, returned {repr(type(resp))} instead')
            resp=Response(addr,b'OK:'+resp,socket.SOCK_DGRAM)
            if debug:
                print('Request '+repr(m)+'from'+ repr(addr)+'->Response '+repr(resp.content)+' to '+repr(resp.addr))
            resp.send()


