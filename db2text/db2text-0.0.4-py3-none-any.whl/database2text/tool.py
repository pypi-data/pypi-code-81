#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,os,difflib

__all__=["db","ckd","cfgdata"]

def mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def quit(errinfo,exitcode=0):
    print(errinfo)
    sys.exit(exitcode)

class dblib(object):
    def res1(self,ssql,*args,**kwargs):
        c=self.conn.cursor()
        c.execute(ssql,*args,**kwargs)
        res=c.fetchone()
        c.close()
        if res==None:
            return
        if len(res)==1:
            return res[0]
        else:
            return res
    def exec(self,ssql,*args,**kwargs):
        c=self.conn.cursor()
        c.execute(ssql,*args,**kwargs)
        return c

class checkdiff(object):
    def init(self,objtype):
        self.diff=difflib.Differ()
        self.objtype=objtype
        self.datadir=cfgdata["datadir"]
        mkdir(self.datadir)
        self.datadir="%s/%s" %(self.datadir,objtype)
        mkdir(self.datadir)
        self.filelist=[]
        for f in os.listdir(self.datadir):
            self.filelist.append(f)
    def comp(self,objname,objdata):
        fn="%s/%s" %(self.datadir,objname)
        if os.path.isfile(fn):
            data=open(fn).read()
            if data==objdata:
                return
            print("============diff of %s.%s" %(self.objtype,objname))
            print("\n".join(self.diff.compare(data.split("\n"),objdata.split("\n"))))
        else:
            print("============find new: %s.%s" %(self.objtype,objname))
            print(objdata)
        with open(fn,"w") as f:
            f.write(objdata)

db=dblib()
ckd=checkdiff()
