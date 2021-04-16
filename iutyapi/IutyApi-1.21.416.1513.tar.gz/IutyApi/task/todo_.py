from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime,os


dbg = os.path.exists("./debug")
debuglist = "3"
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','task',8510)
else:
    mysql = MySql('localhost','root','fastcorp','task')

class Frm_Todo_Data(mysql.Model):
    def addRecord(self,title):
        self.add(value=[{"title":title,"finishdate":None,"filed":0}])
        pass
    
    def finishRecord(self,tid):
        data = self.query(where=r"tid = '{}'".format(tid))
        if len(data) > 0:
            if data[0]["finishdate"] is None:
                today = datetime.date.today()
                self.update(value=[{"finishdate":today}],where=r"tid = '{}'".format(tid))
            else:
                self.update(value=[{"finishdate":None}],where=r"tid = '{}'".format(tid))
        pass
    
    def fileRecord(self,tid):
        self.update(value=[{"filed":1}],where=r"tid = '{}'".format(tid))
        pass
    
    
    
    pass

class Frm_TodoList_Data(mysql.Model):
    def addRecord(self,lid,title):
        db0 = Frm_Todo_Data()
        db0.addRecord(title)
        data_l = db0.query(target=r"max(tid) as tid")
        
        self.add(value=[{"lid":lid,"tid":data_l[0]["tid"]}])
        pass
    
    def deleteRecord(self,lid):
        self.delete(where=r"lid='{}'".format(lid))
        pass
    
    def moveRecord(self,tid,tlid):
        self.update(value=[{"lid":tlid}],where=r"tid='{}'".format(tid))
    
    pass
        
    
class V_TodoList_Data(mysql.Model):
    def queryRecord(self,lid):
        data = self.query(where=r"lid = '{}' and filed = 0".format(lid),orderby = r"finishdate,tid")
        return data
    
    def fileRecord(self,lid):
        data = self.query(where=r"lid = '{}' and filed = 0 and not finishdate is Null".format(lid))
        
        db = Frm_Todo_Data()
        for d in data:
            db.fileRecord(d["tid"])
        pass

class Frm_TodoList_Info(mysql.Model):
    def addRecord(self,lid,name):
        self.add(value=[{"name":name}])
        lid = self.query(target=r"max(lid) as lid")[0]["lid"]
        return lid
    
    def renameTodoList(self,lid,name):
        self.update(value=[{"name":name}],where = r"lid = '{}'".format(lid))
        pass

class Frm_TodoList_Owner(mysql.Model):
    def addRecord(self,lid,uid,type):
        self.add(value=[{"uid":uid,"lid":lid,"type":type,"group1":"未分组","group2":"未分组"}])
    
    def updateGroup(self,lid,uid,group1,group2):
        self.update(value=[{"group1":group1,"group2":group2}],where=r"lid = '{}' and uid = '{}'".format(lid,uid))
    
    def deleteRecord(self,lid,uid):
        self.delete(where=r"uid='{}' and lid = '{}'".format(uid,lid))
    
    def queryGroupEnum(self,uid):
        data = {"group1":[],"group2":[]}
        group1 = self.query(target = r"group1",where=r"uid = '{}'".format(uid),groupby="group1")
        for g in group1:
            data["group1"].append(g["group1"])
        group2 = self.query(target = r"group2",where=r"uid = '{}'".format(uid),groupby="group2")
        for g in group2:
            data["group2"].append(g["group2"])
        return data
    pass

class V_TodoList_Info(mysql.Model):
    def queryRecord(self,uid):
        data = self.query(where=r"uid = '{}'".format(uid))
        return data
    
    def checkDefault(self,uid):
        data = self.queryRecord(uid)
        if len(data) == 0:
            self.addTodoList(uid,0,"待办集")
        pass
    
    def addTodoList(self,uid,type,name):
        lid = Frm_TodoList_Info().addRecord(uid,name)
        
        Frm_TodoList_Owner().addRecord(lid,uid,type)
        pass

class TodoApi(Resource):
    def query():
        rtn = {"success":False}
        lid = request.form.get("lid")
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        data = V_TodoList_Data().queryRecord(lid)
        
        for d in data:
            if not d["finishdate"] == None:
                d["finishdate"] = datetime.datetime.strftime(d["finishdate"],"%Y-%m-%d")
        rtn["data"] = data
        rtn["success"] = True
        return rtn
        
    def finishTodo():
        rtn = {"success":False}
        tid = request.form.get("tid")
        lid = request.form.get("lid")
        if not tid:
            rtn["error"] = "tid is nesserary"
            return rtn
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        Frm_Todo_Data().finishRecord(tid)
        
        rtn["success"] = True
        return rtn
    
    def addTodo():
        rtn = {"success":False}
        title = request.form.get("title")
        lid = request.form.get("lid")
        if not title:
            rtn["error"] = "title is nesserary"
            return rtn
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        Frm_TodoList_Data().addRecord(lid,title)
        
        rtn["success"] = True
        return rtn
    
    def fileTodo():
        rtn = {"success":False}
        lid = request.form.get("lid")
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        V_TodoList_Data().fileRecord(lid)
        rtn["success"] = True
        return rtn
    
    def moveTodo():
        rtn = {"success":False}
        tid = request.form.get("tid")
        
        tlid = request.form.get("tlid")
        if not tid:
            rtn["error"] = "tid is nesserary"
            return rtn
        
        
        if not tlid:
            rtn["error"] = "tlid is nesserary"
            return rtn
        
        Frm_TodoList_Data().moveRecord(tid,tlid)
        rtn["success"] = True
        return rtn
    
    def queryTodoList():
        rtn = {"success":False}
        uid = session.get("uid")
        if not uid:
            uid = 1
        db = V_TodoList_Info()
        db.checkDefault(uid)
        data = db.queryRecord(uid)
        for d in data:
            d["done"] = int(d["done"])
            d["total"] = int(d["total"])
        rtn["success"] = True
        rtn["data"] = data
        return rtn
    
    def queryGroupEnum():
        rtn = {"success":False}
        uid = session.get("uid")
        if not uid:
            uid = 1
        
        db = Frm_TodoList_Owner()
        data = db.queryGroupEnum(uid)
        
        rtn["data"] = data
        rtn["success"] = True
        return rtn
    
    def addTodoList():
        rtn = {"success":False}
        uid = session.get("uid")
        if not uid:
            uid = 1
        
        db = V_TodoList_Info()
        db.checkDefault(uid)
        db.addTodoList(uid,1,"新增待办集")
        
        
        rtn["success"] = True
        return rtn
    
    def renameTodoList():
        rtn = {"success":False}
        lid = request.form.get("lid")
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        name = request.form.get("name")
        if not name:
            rtn["error"] = "name is nesserary"
            return rtn
        
        db = Frm_TodoList_Info()
        db.renameTodoList(lid,name)
        
        
        
        rtn["success"] = True
        return rtn
        
    def updateGroup():
        rtn = {"success":False}
        lid = request.form.get("lid")
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        uid = session.get("uid")
        if not uid:
            uid = 1
        
        group1 = request.form.get("group1")
        if not group1:
            group1 = "未分组"
        
        group2 = request.form.get("group2")
        if not group2:
            group2 = "未分组"
        
        db = Frm_TodoList_Owner()
        db.updateGroup(lid,uid,group1,group2)
        
        
        
        rtn["success"] = True
        return rtn
    
    def removeTodoList():
        rtn = {"success":False}
        lid = request.form.get("lid")
        if not lid:
            rtn["error"] = "lid is nesserary"
            return rtn
        
        uid = session.get("uid")
        if not uid:
            uid = 1
        
        db = Frm_TodoList_Owner()
        db.deleteRecord(lid,uid)
        
        rtn["success"] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        if _cmd == 'queryTodo':
            return TodoApi.query()
        
        if _cmd == 'finishTodo':
            return TodoApi.finishTodo()
        
        if _cmd == 'addTodo':
            return TodoApi.addTodo()
        
        if _cmd == 'fileTodo':
            return TodoApi.fileTodo()
        
        if _cmd == 'moveTodo':
            return TodoApi.moveTodo()
        
        if _cmd == 'removeTodo':
            return TodoApi.removeTodo()
        
        if _cmd == "addTodoList":
            return TodoApi.addTodoList()
        
        if _cmd == "queryTodoList":
            return TodoApi.queryTodoList()
        
        if _cmd == "queryGroupEnum":
            return TodoApi.queryGroupEnum()
        
        if _cmd == "renameTodoList":
            return TodoApi.renameTodoList()
        
        if _cmd == "updateGroup":
            return TodoApi.updateGroup()
        
        if _cmd == "removeTodoList":
            return TodoApi.removeTodoList()
    pass

if __name__ == "__main__":
    
    #Frm_Task_Todo().fileRecord(1)
    #Frm_TodoList_Data().addRecord("2","ttl1")
    d = V_TodoList_Data().queryRecord(3)
    print(d)

