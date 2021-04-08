import socket
import pickle
class Client:
    def __init__(self,addr):
        self.addr=addr
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    def __getattr__(self,attr):
        self.socket.sendto(attr.encode('utf-8'))
        m,addr=self.socket.recvfrom(10000)
        e=""
        if m==b'ERR:ATTR':
            e=AttributeError(f"no attribute {attr} at server")
        try:
            return pickle.loads(m)
        except pickle.UnpicklingError:
            e=ValueError("server returned unpicklable byte field")
        raise e
