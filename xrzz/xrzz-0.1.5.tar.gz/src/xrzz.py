import sock_HTTP_adapter

class http:
    def __init__(self, Reqtype=None, url=None, headers=None, data=None, tls=None):
        self.url = url
        self.Request = Reqtype
        self.headers = headers
        self.data = data
        self.ssl = tls
        
    @property
    def content(self):
        r = sock_HTTP_adapter.Socket(self.Request, self.url, self.headers, self.data, self.ssl)
        return r
        
    def body(self):
        return self.content.Body()

    def head(self):
        kk = self.content.Headers()
        cr = repr(kk)[2:-1].split("\\r\\n")
        del cr[0]
        h = dict()
        for ui in cr: 
            aa = ui.split(": ")
            h[aa[0]] = aa[-1]
        return h
