import socket

class Response:
    def __init__(self,bum,content="",proto=socket.SOCK_RAW):
        if isinstance(bum,Response):
            self=bum
        elif isinstance(bum,tuple):
            self.addr=bum
            
            self.s=socket.socket(socket.AF_INET,proto)
            self.content=content
        else:
            raise TypeError
    def send(self):
        self.s.sendto(self.content,self.addr)
        return self.s.recvfrom(1024)[0]
        
