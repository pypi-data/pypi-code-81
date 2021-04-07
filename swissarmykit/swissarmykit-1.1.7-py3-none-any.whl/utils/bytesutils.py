import codecs

def slashescape(err):
    """ https://qastack.vn/programming/606191/convert-bytes-to-a-string
    codecs error handler. err is UnicodeDecode instance. return
    a tuple with a replacement for the unencodable part of the input
    and a position where encoding should continue"""
    #print err, dir(err), err.start, err.end, err.object[:err.start]
    thebyte = err.object[err.start:err.end]
    repl = u'\\x'+hex(ord(thebyte))[2:]
    return (repl, err.end)

codecs.register_error('slashescape', slashescape)

class BytesUtils:

    @staticmethod
    def bytes_2_str(bytes):
        '''
        Used for subprocess stdout
        '''
        return bytes.decode('utf-8', slashescape)