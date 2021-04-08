import re
import socket
import ssl

class Url:

    def __init__(self, Reqtype, link):
        self.link = link
        self.Request = Reqtype
        
    def Compile(self):
        url_parse = {
            "host":  re.compile("(\w+?[-.].+?)[/]"),
            "query":  re.compile("\w?/[^\/\s]+\/?(.*)"),
            "protocol": re.compile("(\w+)[:]")
        }
        return url_parse
        
    def Regexp(self):
        url = Url.Compile(self)
        List = []
        for Name, RFC in url.items():
            try:
                List.append(RFC.findall(self.link)[0])
            except IndexError:
                return "Invalid Url"
        return List

    def Rectify_Error(self):
        if type(self.Regexp()) is list:
            return self.Regexp()
        else:
            return self.link+'/'
            
    def Proto_check(self):
        if not "https" in self.Regexp()[-1]:
            return 80
        else:
            return 443
            
    @property
    def urlParse(self):
        return {
            'PROTO':self.Proto_check(),
            'HOST':self.Rectify_Error()[0],
            'QUERY':self.Rectify_Error()[1]
        }

class Socket(Url):

    def __init__(self, Reqtype, link, headers=None, data=None, tls=None):
        super(Socket, self).__init__(Reqtype, link)
        Param = {}
        for i, j in self.urlParse.items():
            Param[i] = j
        self.host = Param['HOST']
        self.Request = Reqtype
        self.query = Param['QUERY']
        self.port = Param['PROTO']
        self.headers = headers
        self.data = data
        self.tls = tls

    def Port(self):
        return self.port

    def method(self):
        return self.Request.upper()


    @property
    def Data(self):
        hkl = []
        for _1, _2 in self.data.items():
            hkl.append(_1+"="+_2)
        rc = re.sub(', ', '&', str(hkl)[1:-1]).replace("'", "")
        return ({"Content-Length": len(rc), "Payload": rc})

    @property
    def pack(self):
        if self.headers == None:
            req = "%s /%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: EEE_guys/v1.1\r\nConnection: Close\r\n\r\n" %(self.method(), self.query, self.host)
            return req
        else:
            prwq = re.sub("', '", "\r\n", str(self.headers)).replace("': '", ": ")
            path_head = "%s /%s HTTP/1.1\r\n" %(self.method(), self.query) + prwq[2:-2] + "\r\n\r\n"
            if self.method() == "GET":
                return path_head

## Method POST added

#            else:
#                raise NotImplementedError('method will be implemented in next update')
#                exit()

            else:
                post_head = "%s /%s HTTP/1.1\r\nContent-Length: %s\r\n" %(self.method(), self.query, self.Data["Content-Length"]) + prwq[2:-2] + "\r\n\r\n" + self.Data['Payload']
                return post_head
                
    def Connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 1)
        
        cnt_sock = sock.connect((self.host, self.port))
        if self.tls is True:
            Sl = ssl.create_default_context()
            tls_sock = Sl.wrap_socket(sock, server_hostname=self.host)
            data = tls_sock.send(self.pack.encode("utf-8"))
            chunk = b""
            while True:
                try:
                    dat = tls_sock.recv(0xffff)
                    if not dat: break
                    chunk += dat
                except socket.timeout:
                    exit()
            return chunk
                    
        else:
            sock.send(self.pack.encode())
            chunk1 = b""
            while True:
                hj = sock.recv(0xfff)
                if not hj:
                    break
                chunk1 += hj
            return chunk1

    def Chunk_content(self):
        chunk_body = (re.sub(b"\r\n[\w+]+\r\n", b"\r\n", self.Connect()).split(b"\r\n\r\n"))
        return chunk_body

    def Headers(self):
        return self.Chunk_content()[0]

    def Body(self):
        q1 = self.Chunk_content()
        del q1[0]
        q2 = b"".join(q1)
        body = re.sub(b"\r\n", b"", q2)
        return body
