from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime


dbg = False
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','stock',8510)
else:
    mysql = MySql('localhost','root','fastcorp','stock')

class Frm_Monitor_Data(mysql.Model):
    def addRecord(self,code,target,type,recordusr):
        date = datetime.date.today()
        self.add(value=[{"code":code,"target":float(target),"type":int(type),"recordusr":recordusr,"recorddate":date}])
        pass
    
    def deleteRecord(self,code,type,usr="t.yu"):
        self.delete(where=r"code='{}' and type = '{}' and recordusr = '{}'".format(code,type,usr))
        pass
    
    def replaceRecord(self,code,type,target,recordusr="t.yu"):
        date = datetime.date.today()
        self.replace(value=[{"code":code,"target":float(target),"type":int(type),"recordusr":recordusr,"recorddate":date}],where=r"code='{}' and type = '{}' and recordusr = '{}'".format(code,type,usr))
        pass
    
    def clearRecord(self,recordusr="t.yu"):
        self.delete(where=r"recordusr='{}'".format(recordusr))
        pass
    
    def queryRecord(self):
        data = self.query()
        for d in data:
            d["target"] = float(d["target"])
            d["recorddate"] = datetime.datetime.strftime(d["recorddate"],"%y-%m-%d")
        
        return data
        pass
    pass
    
class MonitorApi(Resource):
    def add():
        rtn = {"success":False}
        _code = request.form.get("code")
        _target = request.form.get("target")
        _type = request.form.get("type")
        _recordusr = request.form.get("recordusr")
        if not _code:
            rtn["error"] = "code is nesserary"
            return rtn
        if not _target:
            rtn["error"] = "target is nesserary"
            return rtn
        if not _type:
            rtn["error"] = "type is nesserary"
            return rtn
        if not _recordusr:
            rtn["error"] = "recordusr is nesserary"
            return rtn
        date = datetime.date.today()
        Frm_Monitor_Data().addRecord(_code,_target,_type,_recordusr)
        
        rtn["success"] = True
        return rtn
    
    def query():
        rtn = {"success":False}
        data = Frm_Monitor_Data().queryRecord()
        
        rtn["data"] = data
        rtn["success"] = True
        return rtn
    
    def delete():
        rtn = {"success":False}
        _code = request.form.get("code")
        if not _code:
            rtn["error"] = "code in nesserary"
            return rtn
        
        _type = request.form.get("type")
        if not _type:
            rtn["error"] = "type in nesserary"
            return rtn
        
        Frm_Monitor_Data().deleteRecord(_code,_type)
        rtn["success"] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        if _cmd == 'query':
            return MonitorApi.query()
        
        if _cmd == 'add':
            return MonitorApi.add()
        
        if _cmd == 'delete':
            return MonitorApi.delete()
    pass

if __name__ == "__main__":
    #Frm_Monitor_Data().addRecord("000002",5.17,"1")
    #Frm_Monitor_Data().deleteRecord("000001")
    Frm_Monitor_Data().queryRecord()

