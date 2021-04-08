import socket
import pickle
class Server:
    def __init__(self,addr):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr=addr
        self.sock.bind(addr)
        self.objs={}
    def add_obj(self,obj):
        e=""
        try:
            self.objs[obj.__name__]=pickle.dumps(obj)
            return
        except:
           e=TypeError("unpicklable type")
        raise e
    def run(self):
        while True:
            m,addr=self.sock.recvfrom(10000)
            b=m.decode('utf-8')
            try:
                o=self.objs[b]
            except KeyError:
                s.sendto(b'ERR:ATTR',addr)
                continue
            s.sendto(o,addr)
            
