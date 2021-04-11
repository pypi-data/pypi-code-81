from io import BytesIO as b
from io import StringIO as s

class ff:
    class Binary:
        file = b()
        def write(self, data):
            self.file.write(data)
        def read(self):
            return self.file.getvalue()
        def writeReal(self, outfile):
            open(outfile, 'wb').write(self.file.getvalue())
        def get(self):
            return self.file.getvalue()
    class Text:
        file = s()
        def write(self, data):
            self.file.write(data)
        def read(self):
            return self.file.getvalue()
        def writeReal(self, outfile):
            open(outfile, 'w').write(self.file.getvalue())
        def get(self):
            return self.file.getvalue()
    
