import os, subprocess, importlib
def testOutDate():
    ret="test"
    import subprocess
    while ret:
        ret = subprocess.getoutput("py -m pip list --outdated")
        if ret:
            print(ret)
            ret = ret.split("\n")
            ret.pop(0)
            ret.pop(0)
            for i in range(len(ret)):
                ret[i] = (ret[i].split(" "))[0]
            temp = "py -m pip install --upgrade "
            for i in range(len(ret)):
                temp+=f"pip {ret[i]} "
            os.system(temp)
            print(temp)
class importing(object):
    """ return a list with all package requiered but without error """
    def importing(data, exeption=None, From=""):
        def getNumber(data, y=len(data), ret=0):
            moin=0
            if data[y].find("(") != -1:
                debut=data[y].find("(")
                fin=data[y].find(")")
                ret = ""
                for i in range(debut+1, fin):
                    moin-=1
                    ret += str(data[y][i])
                moin-=2
                ret = int(ret)
            else:
                ret+=1
            if moin == 0:
                moin=len(data[y])
            return data[y][0:moin], ret
        bas = 0
        loop = 0
        ret = 0
        RET = 0
        retour=[]
        exept=[]
        lenExeption = 0
        if exeption!=None:
            exeption = exeption.split(" ")
            lenExeption = len(exeption)
        From = From.split(" ")
        for y in range(lenExeption):
            if exeption!=None:
                exept, ret = getNumber(exeption, y=y, ret=ret)
            if From!=None:
                FROM, RET = getNumber(From, y=y, ret=RET)
            while loop < len(data.split(" ")):
                loop+=1
                dataLoop=data.split(" ")[loop-1]
                temp = False
                try:
                    try:
                        importlib.import_module(dataLoop)
                    except:
                        importlib.import_module(dataLoop+"."+FROM)
                    temp = True
                except:
                    try:
                        if loop == ret:
                            result = subprocess.getoutput("py -m pip install "+exept)
                        else:
                            result = subprocess.getoutput("py -m pip install "+dataLoop)
                        print(result)
                        if (result.split("\n"))[-1][0:6] == "ERROR:":
                            break
                        temp = True
                    except:
                        pass
                finally:
                    if temp == True:
                        try:
                            retour.append(importlib.import_module(dataLoop))
                        except:
                            print(f"{dataLoop} n'existe pas")
                    else:
                        print(f"{dataLoop} {exept} n'a pas marcher")
                    if loop == ret:
                        break
        while loop < len(data.split(" ")):
            loop+=1
            dataLoop=data.split(" ")[loop-1]
            temp = False
            try:
                try:
                    importlib.import_module(dataLoop)
                except:
                    importlib.import_module(dataLoop+"."+FROM)
                temp = True
            except:
                try:
                    result = subprocess.getoutput("py -m pip install "+dataLoop)
                    print(result)
                    if (result.split("\n"))[-1][0:6] == "ERROR:":
                        break
                    temp = True
                except:
                    pass
            finally:
                if temp == True:
                    try:
                        try:
                            retour.append(importlib.import_module(dataLoop))
                        except:
                            retour.append(importlib.import_module(dataLoop+"."+FROM))
                    except:
                        print(f"{dataLoop} n'existe pas")
                else:
                    print(f"{dataLoop} {exept} n'a pas marcher")
        return retour
    def example():
        importing.importing("colored")
        from colored import fg, bg, attr
        reset = attr(0)
        print(f'\nlist=importing.importing({fg(2)}"module_name1 module_name2"{reset}, {fg(2)}"exeption_name(2)"{reset})\n')
if __name__ == "__main__":
    importing.example()