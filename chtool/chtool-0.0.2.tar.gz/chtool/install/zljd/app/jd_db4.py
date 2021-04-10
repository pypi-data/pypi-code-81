
import time 

from lmf.tool import  mythread
from lmfinstall import common 
from lmfinstall.postgresql import postgresql1061
from lmfinstall.python import python
import copy
from fabric import Connection
from lmf.dbv2 import db_command_ext ,db_command,db_query
import shutil 
from zljd.core.oss import oss 
import os
#20200616京东云从零部署
class jd_db4:
    def __init__(self,local_file_download=True):
        self.pin=[
                    ['root@10.0.64.21:22','BST@2020610','db1'],
                    ['root@10.0.64.22:22','BST@2020610','db2'],
                    ['root@10.0.64.23:22','BST@2020610','db3'],
                    ['root@10.0.64.24:22','BST@2020610','db4'],
                    ]


        self.db_conp=[
        ['postgres','since2015','10.0.64.21','postgres','public'],
        ['postgres','since2015','10.0.64.22','postgres','public'],
        ['postgres','since2015','10.0.64.23','postgres','public'],
        ['postgres','since2015','10.0.64.24','postgres','public']
        ]
        self.oss_internal=True
        self.local_file_dir="D:\\jingdong_db4sys_download"
        self.local_file_download=local_file_download 
        self.init_local_file()

    def init_local_file(self):
        tmpdir=self.local_file_dir
        self.pg_file="%s\\postgresql-10.6-1-linux-x64.run"%tmpdir
        self.python_file="%s\\Python-3.5.2.tgz"%tmpdir

    def down_gpfile(self):
        tmpdir=self.local_file_dir
        if self.local_file_download:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            files=['Python-3.5.2.tgz', 'postgresql-10.6-1-linux-x64.run']
            m=oss(conp='')
            m.internal=self.oss_internal
            for file in files:
                bg=time.time()
                filename='backup/soft/'+file 
                print(file)
                m.down_file(filename,"%s/%s"%(tmpdir,file))
                ed=time.time()
                cost=int(ed-bg)
                print("totoal cost --%d s "%cost)

    def os_prt(self):
        self.os_prt1()
        self.os_prt2()
    def os_prt1(self):
        common.hostname(self.pin)
        common.dns(self.pin)
        common.ssh(self.pin)

    #挂载磁盘
    def os_prt2(self):
        k='/dev/vdb'
        v='/data'
  
        for conp in self.pin :
            print(conp[2])
            
            common.mount(conp,k,v)
    def test(self):   
        for conp in self.pin:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("hostname && ip addr")

    def pg_prt1(self):

        bg=time.time()
        self.down_gpfile()
        def f1(conp):
            postgresql1061.install(conp,self.pg_file,pgdata="/data/postgresql",plpython='plpython35')
        mythread(f=f1,arr=self.pin).run(len(self.pin))

        def f2(conp):
            python.install(conp,self.python_file)
        mythread(f=f2,arr=self.pin).run(len(self.pin))
        ed=time.time()
        cost=int(ed-bg)
        print("totally coast %d s"%cost)
    def pg_prt2(self):
        for conp in self.db_conp:
            try:
                self.pg_prt2_tmp(conp)
            except Exception as e:
                print(e)
    def pg_prt2_tmp(self,conp):
        #创建角色
        extension=['plpython3u','pgcrypto','dblink']
        for ext in extension:
            sql="create extension  if not exists %s"%ext
            print(sql)
            db_command(sql,dbtype="postgresql",conp=conp)

        for user in ['app_reader','zl_reader']:
            sql1="create user app_reader with password 'app_reader';"
            sql2="grant usage on schema public to app_reader;"
            sql3="grant select on all tables in schema public to app_reader;"
            sql=sql1+sql2+sql3
            sql=sql.replace('app_reader',user)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=conp)

    def pg_prt3(self):
        def f1(conp):
            m=oss(conp=conp)
            m.s3fs_pre()
        mythread(f=f1,arr=self.pin).run(len(self.pin))

    def task(self):

        self.os_prt()
        self.pg_prt1()
        self.pg_prt2()
        self.pg_prt3()
def task1():
    from zljd.core.sdk import sdk 
    sdk().rebuild_hosts('pg_db')
    m=jd_db4(True)
    m.task()
if __name__=='__main__':
    #task1()
    jd_db4(False).pg_prt3()
    print("heheh")