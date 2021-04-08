
ospath = "C:\\Users\\felix\\OneDrive\\Desktop\\dev\\python\\pyos\\os\\"

from pathdict import pathdict
from sys import getsizeof
from pympler.asizeof import asizeof



localpath = "C:\\"

paths = pathdict(["C:"], [pathdict()])



def cmd(text: str):
    global localpath
    
    inputlist = text.split(" ")
    inputlen = len(inputlist)
    
    if inputlen == 0:
        return
    
    
    command = inputlist[0]
        
    if command == "mkdir":
        if inputlen == 1:
            print("Required parameter missing")
            print()
            return
            
        newdir = inputlist[1]
        try:
            if "\\" not in newdir:
                newpath = (localpath + newdir).split("\\")
                newpath = paths[newpath[:-1]]
                newpath.append(newdir, pathdict())
        except KeyError:
            print("Directory already exists")
            print()
            return
                
    elif command == "cd":
        if inputlen == 1:
            print(localpath)
            print()
            return
            
        todir = inputlist[1]
        try:
            path = localpath.split("\\")[:-1]
            if todir == "..":
                if len(path) == 1:
                    return
                else:
                    localpath = "\\".join(path[:-1]) + "\\"
            
            elif "\\" not in todir:
                if todir in paths[path]:
                    if not isinstance(paths[path + [todir]], pathdict):
                        raise KeyError
                    
                    localpath += todir + "\\"
                else:
                    raise KeyError
        except KeyError:
            print("Invalid directory")
            print()
            return
                  
    elif command == "dir":
        if inputlen == 1:
            dotpath = localpath.split("\\")[:-1]
            print(". ", "\t\t<DIR>    ", asizeof(paths[dotpath]))
            
            if len(dotpath) == 1:
                print("..", "\t\t<DIR>    ", asizeof(paths))
            else:
                print("..", "\t\t<DIR>    ", asizeof(paths[dotpath[:-1]]))
                
                
            for path, data in paths[dotpath].items():
                if isinstance(data, pathdict):
                    print(path, "\t\t<DIR>    ", asizeof(data))
                else:
                    print(path, "\t\t<FILE>   ", asizeof(data))
                                     
            print()
            
    
    elif command == "rmdir":
        if inputlen == 1:
            print("Required parameter missing")
            print()
            return
            
        deldir = inputlist[1]
        try:
            if "\\" not in deldir:
                delpath = (localpath + deldir).split("\\")
                
                if not isinstance(paths[delpath], pathdict):
                    print("Invalid directory")
                    return
                elif len(paths[delpath]) == 0:
                    paths[delpath[:-1]].delete(deldir)
                else:
                    prompt = input("The specified directory is NOT empty. Are you sure you want to DELETE it (Y/N)? ")
                    if prompt in ["Y", "y", "YES", "yes"]:
                        paths[delpath[:-1]].delete(deldir)
                    else:
                        return
                    
        except KeyError:
            print("Directory doesn't exist")
            print()
            return
    
    elif command == "mk":
        if inputlen == 1:
            print("Required parameter missing")
            print()
            return
            
        newfile = inputlist[1]
        try:
            if "\\" not in newfile:
                newpath = (localpath + newfile).split("\\")
                newpath = paths[newpath[:-1]]
                newpath.append(newfile, b"")
        except KeyError:
            print("File already exists")
            print()
            return
        
    elif command == "rm":
        if inputlen == 1:
            print("Required parameter missing")
            print()
            return
            
        delfile = inputlist[1]
        try:
            if "\\" not in delfile:
                delpath = (localpath + delfile).split("\\")
                
                if isinstance(paths[delpath], pathdict):
                    print("You are trying to delete a directory. Use 'rmdir'")
                    return
                else:
                    paths[delpath[:-1]].delete(delfile)
        except KeyError:
            print("File doesn't exist")
            print()
            return
    
    
    
    elif command == "exit":
        exit()
    
    
    else: return
                        





while True:
    
    text = input(f"{localpath}>")
    cmd(text)
    
    
    