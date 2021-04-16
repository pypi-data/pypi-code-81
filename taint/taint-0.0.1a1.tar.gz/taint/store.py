class FileStore:

    def __init__(self, path):
        self.path = path
        self.initd = False


    def save(self, data):
        f = open(self.path, 'wb')
   
        l = len(data)
        c = 0
        while c < l:
            c += f.write(data[c:])
        f.close()

        self.initd = True
