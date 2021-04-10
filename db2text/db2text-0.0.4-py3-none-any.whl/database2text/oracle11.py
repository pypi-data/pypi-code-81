#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,cx_Oracle
import database2text.tool as dbtt
from database2text.tool import *

class oracle(object):
    def ana_TABLE(otype):
        owner=dbtt.cfgdata['loginname'].upper()
        for oname, in db.exec("select object_name from user_objects where object_type=:ot",ot=otype):
            odata="create table %s\n(\n" %(oname)
            maxcsize=db.res1("select max(length(column_name)) from all_tab_cols where owner='%s' and table_name='%s'" %(owner,oname))
            for column_name,data_type,char_length,data_precision,data_scale,nullable,default_length,data_default in db.exec("select column_name,data_type,char_length,data_precision,data_scale,nullable,default_length,data_default from all_tab_cols where owner='%s' and table_name='%s' order by column_id" %(owner,oname)):
                odata=odata+"  %s%*s" %(column_name,maxcsize-len(column_name)+1," ")
                if data_type=="NUMBER":
                    if data_precision is not None and data_scale is not None:
                        if data_scale==0:
                            odata=odata+"NUMBER(%d)" %(data_precision)
                        else:
                            odata=odata+"NUMBER(%d,%d)" %(data_precision,data_scale)
                    elif data_precision is None and data_scale==0:
                        odata=odata+"INTEGER"
                    else:
                        print(column_name,char_length,data_precision,data_scale)
                        sys.exit(0)
                elif data_type in ("VARCHAR2","VARCHAR","CHAR"):
                    odata=odata+"%s(%d)" %(data_type,char_length)
                elif data_type.startswith("TIMESTAMP"):
                    odata=odata+"%s" %(data_type)
                elif data_type in("DATE","BLOB"):
                    odata=odata+"%s" %(data_type)
                else:
                    print(column_name,data_type,char_length,data_precision,data_scale)
                    sys.exit(0)
                if default_length:
                    odata=odata+" default %s" %(data_default.strip())
                if nullable=="N":
                    odata=odata+" not null"
                odata=odata+",\n"
            odata=odata[:-2]
            odata=odata+"\n);"
            ckd.comp(oname,odata)
            
    def ana_VIEW(otype):
        for oname, in db.exec("select object_name from user_objects where object_type=:ot",ot=otype):
            ckd.comp(oname,getobjtext(otype,oname))

    def getobjtext(otype,oname):
        c=db.conn.cursor()
        c.callproc('DBMS_METADATA.SET_TRANSFORM_PARAM',(-1, 'TABLESPACE',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'STORAGE',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'SEGMENT_ATTRIBUTES',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'PRETTY',False))
        ssql=db.res1("SELECT dbms_metadata.get_ddl(:otype,:oname) FROM DUAL",otype=otype,oname=oname).read()
        return ssql

def run():
    try:
        db.conn=cx_Oracle.connect("%s/%s@%s" %(dbtt.cfgdata["loginname"],dbtt.cfgdata["password"],dbtt.cfgdata["dbserver"]))
    except:
        dbtt.quit("数据库连接错误")
    for i in vars(oracle):
        if i.startswith("ana_"):
            otype=i[4:]
            ckd.init(otype)
            getattr(oracle,i)(otype)
