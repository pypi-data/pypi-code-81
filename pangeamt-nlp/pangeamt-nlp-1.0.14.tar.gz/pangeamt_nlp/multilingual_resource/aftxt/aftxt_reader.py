import pangeamt_nlp.multilingual_resource.aftxt.aftxt

class AfTxtReader:
    def __init__(self, src_lang:str, tgt_lang:str):
        self._src_lang = src_lang
        self._tgt_lang = tgt_lang
        self._inverted = False

    def read(self, left:str, right:str):
        if self._inverted:
            return right, left
        return left, right

    def get_src_lang(self):
        return self._src_lang
    src_lang = property(get_src_lang)

    def get_tgt_lang(self):
        return self._tgt_lang
    tgt_lang = property(get_tgt_lang)