from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime

from IutyProxy.stock.ResistanceProxy import ResistanceProxy
from IutyApi.stock.monitor_ import Frm_Monitor_Data

dbg = False
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','stock',8510)
else:
    mysql = MySql('localhost','root','fastcorp','stock')


class Srv_Resistance_Data(mysql.Model):
    def queryRecord(self):
        data = self.query()
        return data
        
    def addRecord(self,code,pu,pd,trend):
        self.add(value=[{"code":code,"pu":pu,"pd":pd,"trend":trend,"au":0,"ad":0}])
        pass
    
    def updateRecord(self,code,pu,pd,trend):
        self.update(value=[{"pu":pu,"pd":pd,"trend":trend}],where=r"code='{}'".format(code))
        pass
    
    def deleteRecord(self,code):
        self.delete(where=r"code = '{}'".format(code))
        pass
    
    def setMonitor(self,code,au,ad):
        self.update(value=[{"au":au,"ad":ad}],where=r"code='{}'".format(code))
    pass

    
class ResistanceApi(Resource):
    #srv_resistance_data
    def query():
        rtn = {"success":False}
        data = Srv_Resistance_Data().queryRecord()
        for d in data:
            d["pu"] = round(float(d["pu"]),2)
            d["pd"] = round(float(d["pd"]),2)
            d["trend"] = int(d["trend"])
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def inquery():
        rtn = {"success":False}
        code = request.form.get("code")
        if not code:
            rtn["error"] = "code is nesserary"
            return rtn
        
        try:
            pu,pd,trend = ResistanceProxy.getResistance(code)
            rtn["data"] = {"pu":pu,"pd":pd,"trend":trend}
            rtn["success"] = True
        except Exception as err:
            rtn["error"] = "inquery error "+str(err)
        return rtn
    
    def update():
        rtn = {"success":False}
        qr = ResistanceApi.query()
        for d in qr["data"]:
            try:
                pu,pd,trend = ResistanceProxy.getResistance(d["code"])
                Srv_Resistance_Data().updateRecord(d["code"],pu,pd,trend)
            except Exception as err:
                print(str(err))
        
        rtn["success"] = True
        return rtn
    
    def follow():
        rtn = {"success":False}
        code = request.form.get("code")
        if not code:
            rtn["error"] = "code is nesserary"
            return rtn
        
        try:
            pu,pd,trend = ResistanceProxy.getResistance(code)
            Srv_Resistance_Data().addRecord(code,pu,pd,trend)
            rtn["success"] = True
        except Exception as err:
            rtn["error"] = "inquery error " + str(err)
        
        return rtn
    
    def unfollow():
        rtn = {"success":False}
        code = request.form.get("code")
        if not code:
            rtn["error"] = "code is nesserary"
            return rtn
        
        Srv_Resistance_Data().deleteRecord(code)
        rtn["success"] = True
        return rtn
    
    #frm_resistance_monitor
    def setMonitor():
        rtn = {"success":False}
        code = request.form.get("code")
        if not code:
            rtn["error"] = "code is nesserary"
            return rtn

        au = request.form.get("au")
        if not au:
            rtn["error"] = "au is nesserary"
            return rtn

        ad = request.form.get("ad")
        if not ad:
            rtn["error"] = "status is nesserary"
            return rtn
        
        Srv_Resistance_Data().setMonitor(code,au,ad)

        rtn["success"] = True
        return rtn
    
    def updateMonitor():
        rtn = {"success":False}
        db1 = Frm_Monitor_Data()
        db1.clearRecord("a.r")
        
        db0 = Srv_Resistance_Data()
        data = db0.queryRecord()
        print(data)
        for d in data:
            if int(d["au"]) == 1:
                db1.addRecord(d["code"],d["pu"],1,"a.r")
            if int(d["ad"]) == 1:
                db1.addRecord(d["code"],d["pd"],0,"a.r")
        
        rtn["success"] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get("cmd")
        if _cmd == "query":
            return ResistanceApi.query()
        
        if _cmd == "inquery":
            return ResistanceApi.inquery()
        
        if _cmd == "follow":
            return ResistanceApi.follow()
        
        if _cmd == "unfollow":
            return ResistanceApi.unfollow()
        
        if _cmd == "setMonitor":
            return ResistanceApi.setMonitor()
        
        if _cmd == "update":
            return ResistanceApi.update()
        
        if _cmd == "updateMonitor":
            return ResistanceApi.updateMonitor()
    pass
    
if __name__ == "__main__":
    db = Srv_Resistance_Data()
    db.setMonitor("600703",1,0)
    #print(db.queryRecord())

    
    pass