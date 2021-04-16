import base64
class CloseError(OSError):
    pass
class AlreadyClosedError(CloseError):
    pass
class IsClosedError(CloseError):
    pass
class _Tag:
    def __init__(self,tag,**attrs):
        self.tag=tag
        self.attrs=attrs
        self.content=''
    def clear_content(self):
        self.content=''
    def write(self,content):
        self.content+=content
    def _out(self):
        attrstr=' '
        for i in self.attrs:
            attrstr+=i+'="'+self.attrs[i]+'" '
        attrstr=attrstr.rstrip()
        return '<'+self.tag+attrstr+'>'+self.content+'</'+self.tag+'>'
class HTML(_Tag):
    def __init__(self,intag='html'):
        super(HTML,self).__init__(intag)
        self._alltags=[]
    def open(self,tag):
        return HTML(intag=tag)
    def commit(self,tag):
        self.content+=tag._out()
        self._alltags+=[tag]
    def output(self):
        return self._out()
    @property
    def data_link(self):
        b64 = base64.b64encode(self.output()).decode()
        return f'data:text/html,{b64}'
    def open_in_browser(self):
        import webbrowser as _wbr
        b64 = base64.b64encode(self.output()).decode()
        _wbr.open(f'data:text/html,{b64}')
    def get_tags(self):
        return self._alltags
    def set_tags(self,taglist):
        self.content=''
        self._alltags = taglist
        for i in taglist:
            if isinstance(i,HTML):
                self.content+=i._out()
            elif isinstance(i,str):
                self.content+=i
            else:
                self.content+=str(i)
def formated(html):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(html, 'lxml')
    return soup.prettify()
