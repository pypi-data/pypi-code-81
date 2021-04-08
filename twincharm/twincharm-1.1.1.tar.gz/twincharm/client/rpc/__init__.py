import socket
import locale
from twincharm.response import Response
class Client:
    def __init__(self):

        self.server=None
        self.funs={}
    def pair(self,server):
        self.server=server
            
    def __getattr__(self,a):
        print('requesting')
        def decor(cargo=b''):
            resp=Response(self.server,a.encode(locale.getpreferredencoding())+b':'+cargo,socket.SOCK_DGRAM)
            b=resp.send()
            if b.startswith(b'ERR:'):
                raise AttributeError
            return b 
            
            
        return decor
            

