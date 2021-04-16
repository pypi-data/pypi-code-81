import httplib2,locale,json
from .speech import say
_URL="https://translate.googleapis.com/translate_a/single?client=gtx&ie={pe}&oe={pe}dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=qc&sl={sl}&tl={tl}&hl={tl}&q={string}"
class TooManyRequestsError(ValueError):pass
class Result:
    def __init__(self,s,l):
        self.result=s
        self._lang=l
        self._re=None
    def __repr__(self):
        return 'Result({})'.format(self.result)
    def __str__(self):
        return self.result
    def __del__(self):
        if self._re is not None:
            self._re.cleanup()
    def say(self):
        self._re=say(self.result,lang=self._lang,hard=True)
class Translator:
    def __init__(self,sl,tl):
        self._pe=locale.getpreferredencoding()
        self._h=httplib2.Http('.cache')
        self.sl=sl
        self.tl=tl
    def translate(self,string):
        u=_URL.format(pe=self._pe,sl=self.sl,tl=self.tl,string=string)
        resp,c=self._h.request(u)
        if resp.status==419:
            raise TooManyRequestsError('server replied 419. Try again later')
        return Result(json.loads(c.decode(self._pe))[0][0][0],self.tl)
def translate(sl,tl,string):
    t=Translator(sl,tl)
    return t.translate(string)
