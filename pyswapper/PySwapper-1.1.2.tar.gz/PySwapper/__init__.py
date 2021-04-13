import pickle,os,sys
class swapper:
    """Creates a swapper object that stores variables in dirpath
    use swapper.varname = value to store value
    and swapper.varname to load them.
    """
    def __init__(s,dirpath:str,erase=True):
        if not dirpath.endswith("\\"):dirpath+="\\"
        if not os.path.exists(dirpath):os.mkdir(dirpath)#create the folder if it doesn't exist
        s._dir=dirpath
        s._e=erase
    def erase(s):
        """deletes every variable in dirpath
        
        warning:this will remove everything in dirpath. not only variables
        """
        for file in tuple(os.walk(s._dir))[0][-1]:
            os.remove(s._dir+file)
    def _getvar(s,name):
        try:
            with open(s._dir+name+".swap","rb") as file:
                data=pickle.load(file)
        except:pass
        else:return data
        raise NameError("name {} is not defined".format(name))
    def _setvar(s,name,value):
        with open(s._dir+name+".swap","wb") as file:
            pickle.dump(value,file)
    def __getattribute__(s,name):
        if name.startswith("_") or name=="erase":return object.__getattribute__(s,name) #use normal get attribute when its not an user-defined one$
        return s._getvar(name)
    def __setattr__(s,name,value):
        if name.startswith("_") or name=="erase":object.__setattr__(s,name,value) #use normal set attribute when its not an user-defined one#
        s._setvar(name,value)
    def __enter__(s):#used for with as statement
        return s
    def __exit__(s,et,ev,t):#simply ignore every exception and erase variables
        if s._e:s.erase()
        return False
