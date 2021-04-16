from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime,os


dbg = os.path.exists("./debug")
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','dev',8510)
else:
    mysql = MySql('localhost','root','fastcorp','dev')

class Frm_Api_Data(mysql.Model):
    def queryRecord(self):
        data0 = self.query()
        data = {}
        for d0 in data0:
            if not d0["namespace"] in data:
                data[d0["namespace"]] = []
            data[d0["namespace"]].append(d0)
        return data
    
    def queryNamespaces(self):
        data = self.query(target=r"namespace")
        return data
    
    def queryApiInfo(self,aid):
        data = self.query(where=r"aid = '{}'".format(aid))
        return data
    
    def updateRecord(self,aid,name,namespace,url,description):
        if str(aid)[0] == "*":
            self.add(value=[{"name":name,"namespace":namespace,"url":url,"description":description}])
        else:
            self.update(value=[{"name":name,"namespace":namespace,"url":url,"description":description}],where=r"aid='{}'".format(aid))
        data = self.query(where=r"name='{}' and namespace = '{}'".format(name,namespace),orderby = "aid desc")
        return data
    
    def deleteRecord(self,aid):
        self.delete(where=r"aid='{}'".format(aid))
        pass
    pass

class Frm_Api_Param(mysql.Model):
    def queryRecord(self,aid):
        data0 = self.query(where=r"aid = '{}'".format(aid))
        data = {}
        for d0 in data0:
            if not d0["direction"] in data:
                data[d0["direction"]] = []
            data[d0["direction"]].append(d0)
        return data
    
    def updateRecord(self,aid,apid,key,direction,description):
        if str(apid) == "0":
            
            self.add(value=[{"aid":aid,"key":key,"direction":direction,"description":description}])
        else:
            self.update(value=[{"key":key,"direction":direction,"description":description}],where=r"apid='{}'".format(apid))
        
        pass
    
    def deleteRecord(self,apid):
        self.delete(where=r"apid='{}'".format(apid))
        pass
    
    def deleteApi(self,aid):
        self.delete(where=r"aid='{}'".format(aid))
        pass
    
    
class Frm_Api_Example_Data(mysql.Model):
    def queryRecord(self,aid):
        data = self.query(where = r"aid = '{}'".format(aid))
        return data
        
    def updateRecord(self,aid,name,eid,description):
        if str(eid) == "0":
            self.add(value=[{"aid":aid,"name":name,"description":description}])
        else:
            self.update(value=[{"name":name,"description":description}],where=r"eid='{}'".format(eid))
        pass
    
    def deleteRecord(self,eid):
        self.delete(where=r"eid='{}'".format(eid))
        pass
    
    def deleteApi(self,aid):
        self.delete(where=r"aid='{}'".format(aid))
        pass
    
class Frm_Api_Example_Param(mysql.Model):
    def queryRecord(self,eid):
        data = self.query(where = r"eid = '{}'".format(eid))
        return data
        
    def updateRecord(self,eid,apid,value,enabled):
        
        self.replace(value=[{"eid":eid,"apid":apid,"value":value,"enabled":enabled}])
        pass
    
    def deleteExample(self,eid):
        self.delete(where=r"eid='{}'".format(eid))
        pass
    
    def deleteApiParam(self,apid):
        self.delete(where=r"apid='{}'".format(apid))
        pass
    
    def deleteRecord(self,apid,eid):
        self.delete(where=r"apid='{}' and eid='{}'".format(apid,eid))
        pass

class V_Api_Example_Param(mysql.Model):
    def queryRecord(self,eid):
        data = self.query(where = r"eid = '{}' and direction = '0'".format(eid),orderby = "enabled desc")
        for d in data:
            
            if d['enabled'] == 1:
                d['enabled'] = True
            else:
                d['enabled'] = False
        return data

class V_Api_Example_Data(mysql.Model):
    def queryRecord(self,aid):
        data = self.query(where = r"aid = '{}'".format(aid))
        return data
    
class ApiApi(Resource):
    def getApis():
        rtn = {"success":False}
        
        db = Frm_Api_Data()
        data = db.queryRecord()
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def getApiInfo():
        rtn = {"success":False}
        aid = request.form.get('aid')
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        db = Frm_Api_Data()
        data = db.queryApiInfo(aid)
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def deleteApiInfo():
        rtn = {"success":False}
        aid = request.form.get('aid')
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        db = Frm_Api_Data()
        data = db.deleteRecord(aid)
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def getNamespaces():
        rtn = {"success":False}
        
        db = Frm_Api_Data()
        data = db.queryNamespaces()
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def updateApiInfo():
        rtn = {"success":False}
        aid = request.form.get("aid")
        name = request.form.get("name")
        namespace = request.form.get("namespace")
        url = request.form.get("url")
        description = request.form.get("description")
        debugurl = request.form.get("debugurl")
        
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        if not name:
            rtn["error"] = "name is nesserary"
            return rtn
        
        if not namespace:
            rtn["error"] = "namespace is nesserary"
            return rtn
        
        if not url:
            rtn["error"] = "url is nesserary"
            return rtn
        
        if not description:
            rtn["error"] = "description is nesserary"
            return rtn
        
        db = Frm_Api_Data()
        db.updateRecord(aid,name,namespace,url,description)
        
        rtn['success'] = True
        
        return rtn
    
    def getApiParam():
        rtn = {"success":False}
        aid = request.form.get("aid")
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        db = Frm_Api_Param()
        data = db.queryRecord(aid)
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    
    def updateApiParam():
        rtn = {"success":False}
        aid = request.form.get("aid")
        apid = request.form.get("apid")
        
        key = request.form.get("key")
        
        direction = request.form.get("direction")
        description = request.form.get("description")
        
        
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        if not key:
            rtn["error"] = "key is nesserary"
            return rtn
        
        if not apid:
            rtn["error"] = "apid is nesserary"
            return rtn
        
        if not direction:
            rtn["error"] = "direction is nesserary"
            return rtn
        
        if not description:
            rtn["error"] = "description is nesserary"
            return rtn
        
        db = Frm_Api_Param()
        db.updateRecord(aid,apid,key,direction,description)
        
        
        rtn['success'] = True
        
        return rtn
    
    def deleteApiParam():
        rtn = {"success":False}
        
        apid = request.form.get("apid")
        
        if not apid:
            rtn["error"] = "apid is nesserary"
            return rtn
        
        db = Frm_Api_Param()
        db.deleteRecord(apid)
        
        db = Frm_Api_Example_Param()
        db.deleteApiParam(apid)
        
        rtn['success'] = True
        
        return rtn
    
    def getExample():
        rtn = {"success":False}
        aid = request.form.get("aid")
        
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
        db = V_Api_Example_Data()
        data = db.queryRecord(aid)
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def updateExample():
        rtn = {"success":False}
        aid = request.form.get("aid")
        name = request.form.get("name")
        eid = request.form.get("eid")
        
        description = request.form.get("description")
        
        
        if not aid:
            rtn["error"] = "aid is nesserary"
            return rtn
            
        if not name:
            rtn["error"] = "name is nesserary"
            return rtn
        
        if not eid:
            rtn["error"] = "eid is nesserary"
            return rtn
        
        if not description:
            rtn["error"] = "description is nesserary"
            return rtn
        
        db = Frm_Api_Example_Data()
        db.updateRecord(aid,name,eid,description)
        
        rtn['success'] = True
        
        return rtn
    
    def deleteExample():
        rtn = {"success":False}
        eid = request.form.get("eid")
        
        if not eid:
            rtn["error"] = "eid is nesserary"
            return rtn
        db = Frm_Api_Example_Data()
        data = db.deleteRecord(eid)
        
        db = Frm_Api_Example_Param()
        data = db.deleteExample(eid)
        
        rtn["success"] = True
        
        return rtn
    
    def getExampleParam():
        rtn = {"success":False}
        eid = request.form.get("eid")
        if not eid:
            rtn["error"] = "eid is nesserary"
            return rtn
        
        db = V_Api_Example_Param()
        data = db.queryRecord(eid)
        
        
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def updateExampleParam():
        rtn = {"success":False}
        eid = request.form.get("eid")
        apid = request.form.get("apid")
        
        value = request.form.get("value")
        enabled = request.form.get("enabled")
        
        
        if not eid:
            rtn["error"] = "eid is nesserary"
            return rtn
        
        if not apid:
            rtn["error"] = "apid is nesserary"
            return rtn
        
        enabled = int(bool(enabled))
        
        
        db = Frm_Api_Example_Param()
        db.updateRecord(eid,apid,value,enabled)
        
        rtn['success'] = True
        
        return rtn
    

    
    def post(self):
        _cmd = request.form.get('cmd')
        if _cmd == 'getApis':
            return ApiApi.getApis()
        
        if _cmd == 'getApiInfo':
            return ApiApi.getApiInfo()
        
        if _cmd == 'getNamespaces':
            return ApiApi.getNamespaces()
        
        if _cmd == 'updateApiInfo':
            return ApiApi.updateApiInfo()
        
        if _cmd == 'deleteApiInfo':
            return ApiApi.deleteApiInfo()
        
        if _cmd == 'getApiParam':
            return ApiApi.getApiParam()
        
        if _cmd == 'updateApiParam':
            return ApiApi.updateApiParam()
        
        if _cmd == 'deleteApiParam':
            return ApiApi.deleteApiParam()
        
        if _cmd == 'updateExample':
            return ApiApi.updateExample()
        
        if _cmd == 'getExample':
            return ApiApi.getExample()
        
        if _cmd == 'deleteExample':
            return ApiApi.deleteExample()
        
        if _cmd == 'updateExampleParam':
            return ApiApi.updateExampleParam()
        
        if _cmd == 'getExampleParam':
            return ApiApi.getExampleParam()
        
        if _cmd == 'testExample':
            return ApiApi.testExample()
        
        if _cmd == 'getJqCode':
            return ApiApi.getJqCode()
    pass

if __name__ == "__main__":
    pass

