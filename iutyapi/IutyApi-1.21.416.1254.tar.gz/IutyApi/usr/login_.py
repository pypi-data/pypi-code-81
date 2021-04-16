from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime,os


dbg = os.path.exists("./debug")
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','usr',8510)
else:
    mysql = MySql('localhost','root','fastcorp','usr')

class Srv_Login_Password(mysql.Model):
    def addRecord(self,usr,psw):
        self.replace(value=[{"usr":usr,"psw":psw}])
        pass
    
    def queryRecord(self,usr):
        data = self.query(where=r"usr='{}'".format(usr))
        return data
    
    def updateRecord(self,usr,psw):
        self.update(value=[{"psw":psw}],where=r"usr='{}'".format(usr))
        pass
    pass
    
class LoginApi(Resource):
    def addUsr():
        rtn = {"success":False}
        usr = request.form.get("usr")
        if not usr:
            rtn["error"] = "usr is nesserary"
            return rtn
        
        Srv_Login_Password().addRecord(usr,"777777")
        
        rtn["success"] = True
        return rtn
    
    def login():
        rtn = {"success":False}
        usr = request.form.get("usr")
        psw = request.form.get("psw")
        
        if not usr:
            rtn["error"] = "usr is nesserary"
            return rtn
            
        if not psw:
            rtn["error"] = "psw is nesserary"
            return rtn
        
        data = Srv_Login_Password().queryRecord(usr)
        
        if len(data) > 0:
            if data[0]["psw"] == psw:
                #login ok
                session["usr"] = usr
                session["uid"] = data[0]["uid"]
                rtn["success"] = True
                return rtn
            else:
                #login failed
                rtn["error"] = "user and password is not matched"
                return rtn
        else:
            rtn["error"] = "user is not exists"
            return rtn
    
    def reset():
        rtn = {"success":False}
        usr = request.form.get("usr")
        if not usr:
            usr = session.get("usr")
        if not usr:
            rtn["error"] = "usr in nesserary"
            return rtn
        
        Srv_Login_Password().updateRecord(usr,"777777")
        rtn["success"] = True
        return rtn
    
    def modifyPassword():
        rtn = {"success":False}
        usr = session.get("usr")
        psw = request.form.get("psw")
        if not usr:
            rtn["error"] = "modify api must in login mode"
            return rtn
        
        if not psw:
            rtn["error"] = "psw is nesserary"
            return rtn
        Srv_Login_Password().updateRecord(usr,psw)
        rtn["success"] = True
        return rtn
    
    def quit():
        rtn = {"success":False}
        session.clear()
        
        rtn["success"] = True
        return rtn
    
    def status():
        rtn = {"success":False}
        uid = session.get("uid")
        data = {"login":False}
        if uid:
            data["login"] = True
        rtn["data"] = data
        rtn["success"] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        if _cmd == 'addUsr':
            return LoginApi.addUsr()
            
        if _cmd == 'login':
            return LoginApi.login()
        
        if _cmd == 'reset':
            return LoginApi.reset()
        
        if _cmd == 'modifyPsw':
            return LoginApi.modifyPassword()
        
        if _cmd == 'quit':
            return LoginApi.quit()
        
        if _cmd == 'status':
            return LoginApi.status()
    pass

if __name__ == "__main__":
    print(Srv_Login_Password().queryRecord("t.yu"))

