from os import path
print('Loading Simplesavelib')

#exceptions
class ErrorWhileLoadingFile(FileExistsError):
    pass
class BranchAlredyExistException(Exception):
    pass
class IllegalCharactersException(Exception):
    pass
class FunctionReadbranchesNotUsed(Exception):
    pass
class BranchNotFoundError(Exception):
    pass

#branch
class branchsave:
    def containsillegalcharacters(self, text):
        if ',' in text:
            return True
        else:
            return False
    filename = ''
    fileexists = False
    branches = {}
    branchnames = []
    branchstring = ''
    def __init__(self,filename):
        self.filename = filename
        return
    def refreshfile(self):
        self.fileexists = path.isfile(self.filename)
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        read = open(self.filename, 'r')
        branchname = ''
        alltext = read.readlines()
        for i in alltext:
            self.branchstring = self.branchstring + i
            if not i == '':
                ftext = i.split('=')
                branchname = ftext[0]
                self.branchnames.append(branchname)
                try:
                    branchtext = ftext[1]
                    self.branches[branchname] = branchtext
                except:
                    self.branches[branchname] = ''
        return
    def newbranch(self, branchname):
        self.refreshfile()
        if branchname in self.branchnames:
            raise BranchAlredyExistException
            return
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        if self.containsillegalcharacters(branchname) == True:
            raise IllegalCharactersException
            return
        write = open(self.filename, 'a')
        write.write('\n' + branchname + '=')
        write.close()
        self.branchnames.append(branchname)
        return
    def editbranch(self, branchname, text):
        self.refreshfile()
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        read = open(self.filename, 'r')
        alltext = read.readlines()
        goodtext = ''
        for i in alltext:
            temp = i.split('=')
            if temp[0] == branchname:
                goodtext = goodtext + temp[0] + '=' + text + '\n'
            else:
                goodtext = goodtext + i
        write = open(self.filename, 'w')
        write.write(goodtext)
        self.refreshfile()

    def removebranch(self, branchname):
        self.refreshfile()
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        read = open(self.filename, 'r')
        alltext = read.readlines()
        goodtext = ''
        for i in alltext:
            temp = i.split('=')
            if temp[0] == branchname:
                pass
            else:
                goodtext = goodtext + i
        write = open(self.filename, 'w')
        write.write(goodtext)
        self.refreshfile()
    def getcontent(self, branchname):
        self.refreshfile()
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        read = open(self.filename, 'r')
        for i in read.readlines():
            i = i.split('=')
            if i[0] == branchname:
                return i[1].rstrip('\n').split(',')
    def addtobranch(self, branchname, text):
        self.refreshfile()
        if not self.fileexists:
            raise ErrorWhileLoadingFile
            return
        read = open(self.filename, 'r')
        alltext = read.readlines()
        goodtext = ''
        for i in alltext:
            temp = i.split('=')
            if temp[0] == branchname:
                goodtext = goodtext + temp[0] + '=' + temp[1].rstrip('\n') + ',' + text + '\n'
            else:
                goodtext = goodtext + i
        write = open(self.filename, 'w')
        write.write(goodtext)
        self.refreshfile()

print('Simplesavelib has been loaded')
