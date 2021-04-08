import os

class Pfile():
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.fullpath = path + "\\" + filename
        

    def load(self):
        with open(self.fullpath, "r") as f:
            return f.readlines()

    def write(self, *args):
        for arg in args:
            if isinstance(arg, list):
                with open(self.fullpath, "r+") as f:
                    l = f.readlines()
                l[arg[1]] = str(arg[0]) + "\n"
                with open(self.fullpath, "w") as fw:
                    fw.writelines(l)
            else:
                with open(self.fullpath, "a") as f:
                    f.write(str(arg + "\n"))

    def inser(self, *args: list):
        for arg in args:
            with open(self.fullpath, "r+") as f:
                l = f.readlines()
            l.insert(arg[1], str(arg[0]) + "\n")
            with open(self.fullpath, "w") as fw:
                fw.writelines(l)

    def clear(self, *lines: int):
        with open(self.fullpath, "r+") as f:
            l = f.readlines()
            for line in lines:
                l[line] = ""
        with open(self.fullpath, "w") as fw:
            fw.writelines(l)
    
    def delete(self):
        os.remove(self.fullpath)