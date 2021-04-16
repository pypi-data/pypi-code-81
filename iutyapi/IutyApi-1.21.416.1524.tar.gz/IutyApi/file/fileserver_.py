from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime,os,time,base64,json

fileserverpath = r"e:/fs/"

def createDir():
    t = time.time()
    t = str(int(t*100))
    dirname = base64.encodebytes(t.encode('utf8'))
    dirname = str(path,encoding="utf-8").strip()
    
    dirpath = os.path.join(fileserverpath,dirname)
    os.mkdir(dirpath)
    
    return dirname

def getPullList(res,tag = None):
    path_index = os.path.join(fileserverpath,"index","{}.json".format(res))
    if os.path.exists(path_index):
        raise Exception("index is not exists")
    f = open(path_index,"r")
    obj_list = json.load(f)
    if tag:
        if tag in obj_list:
            return obj_list[tag]
    
    keys = obj_list.keys()
    if len(keys) == 0:
        raise Exception("json have no records")
    return obj_list[keys[-1]]

class FileServerApi(Resource):
    """
    File Server reply a file resource service
    No Usr confirm
    No Git
    """
    
    def push():
        """
        push directory to remote
        create a new directory
        """
        dirname = createDir()
        return dirname
    
    def pull():
        """
        pull directory from remote
        """
        index = request.form.get("index")
        tag = request.form.get("tag")
        
        if not index:
            raise Exception("index is nesserary")
        
        return getPullList(res,tag)
        
    
    def append():
        """
        append a file to [tag/last]
        """
        pass
    
    def fetch():
        """
        fetch a file from [tag/last]
        """
        
        pass
    
    def tag():
        """
        set tag to resource
        """
        pass
    
    def lists():
        """
        list resource
        """
        
        pass
    
    def response_post():
        cmd = request.form.get('cmd')
        if "push" == cmd:
            return FileServerApi.push()
        
        if "pull" == cmd:
            return FileServerApi.pull()
        
        if "append" == cmd:
            return FileServerApi.append()
        
        if "fetch" == cmd:
            return FileServerApi.fetch()
        
        if "tag" == cmd:
            return FileServerApi.tag()
        
        if "list" == cmd:
            return FileServerApi.lists()
    
    def post():
        rtn = {"success":False}
        try:
            data = FileServerApi.response_post()
            rtn["success"] = True
            if data:
                rtn["data"] = data
                
        except Exception as err:
            rtn["error"] = err
        
        return rtn

if __name__ == "__main__":
    print(getNewDirName())