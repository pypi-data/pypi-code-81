##负责定时备份文件 
import os 
from zljd.settings import gp_settings
import copy
from datetime import datetime  
from fabric import Connection
from lmf.tool import mythread 
from threading import Thread
from lmf.dbv2 import db_command,db_query
import time ,re
import psycopg2
from collections import defaultdict
from zljd.core.oss import oss 


##在window上 和 linux都能跑，程序执行在linux上
class backup:

    def __init__(self,loc='aliyun',app='app5'):
        self.loc=loc
        self.app=app
        if app!='web':
            self.conp=copy.deepcopy(gp_settings[loc]['conp_%s'%app])
            self.conp_ssh=copy.deepcopy(gp_settings[loc]['conp_%s_ssh'%app])
            self.superuser=copy.deepcopy(gp_settings[loc]['conp_%s_superuser'%app])
        else:
            self.conp_ssh=copy.deepcopy(gp_settings[loc]['conp_web_ssh'])


        self.file_dir="/jdoss/backup"+"/"+app
        if app in ['app5','gp']:
            self.pg_dump_dir="/usr/local/greenplum-db/bin"
        elif app in ["app1",'db1','db2','db3','db4']:
            self.pg_dump_dir="/opt/PostgreSQL/10/bin"
        self.m_oss=oss(conp=self.conp_ssh)
        if self.loc!='jdyun':self.m_oss.internal=False
    def pre_oss(self):
        self.m_oss.s3fs_pre()

    def get_suffix(self):
        suffix=datetime.strftime(datetime.now(),'%Y%m%d')
        return suffix 

    def tb(self,name):
        bg=time.time()
        try:
            self.m_oss.mount()

            conp=self.conp_ssh
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            suffix=self.get_suffix()
            user,password,ip,db,schema=self.conp
            arr=ip.split(":")
            host=arr[0]
            port='5432' if len(arr)==1 else arr[1]


            #(set PGPASSWORD=zhulong!123) & pg_dump -U developer -h 192.168.4.183 -d base_db -F c -v -t dm.qy_base -f
            file="%s/%s_tb_%s.dmp"%(self.file_dir,self.app,name+'_'+suffix)

            if self.app  not in ['app5','gp']:
                cmd="export PGPASSWORD='%s' && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -t %s -f %s"%(password,self.pg_dump_dir,user,host,port,db,name,file)
                cmd1="export PGPASSWORD=*** && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -t %s -f %s"%(self.pg_dump_dir,user,host,port,db,name,file)
            else:
                cmd=""" su -l %s -c  "export PGPASSWORD='%s' && pg_dump -U %s -h %s -p %s -d %s -F c -v -t %s -f %s"  """%(self.superuser,password,user,host,port,db,name,file)
                cmd1="""su -l %s -c "export PGPASSWORD=*** && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -t %s -f %s" """%(self.superuser,self.pg_dump_dir,user,host,port,db,name,file)
            
            print(cmd)
            c.run(cmd,pty=True)
        except Exception as e:
            print(e)
        finally:
            self.m_oss.umount()

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)


    def schema(self,name):
        bg=time.time()
        try:
            self.m_oss.mount()

            conp=self.conp_ssh
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            suffix=self.get_suffix()
            user,password,ip,db,schema=self.conp
            arr=ip.split(":")
            host=arr[0]
            port='5432' if len(arr)==1 else arr[1]


            #(set PGPASSWORD=zhulong!123) & pg_dump -U developer -h 192.168.4.183 -d base_db -F c -v -t dm.qy_base -f
            file="%s/%s_schema_%s.dmp"%(self.file_dir,self.app,name+'_'+suffix)

            if self.app  not in ['app5','gp']:
                cmd="export PGPASSWORD='%s' && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -n %s -f %s"%(password,self.pg_dump_dir,user,host,port,db,name,file)
                cmd1="export PGPASSWORD=*** && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -n %s -f %s"%(self.pg_dump_dir,user,host,port,db,name,file)
            else:
                cmd="""su -l %s -c "export PGPASSWORD='%s' && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -n %s -f %s" """%(self.superuser,password,self.pg_dump_dir,user,host,port,db,name,file)
                cmd1="export PGPASSWORD=*** && %s/pg_dump -U %s -h %s -p %s -d %s -F c -v -n %s -f %s"%(self.pg_dump_dir,user,host,port,db,name,file)
            print(cmd)
            c.run(cmd,pty=True)
        except Exception as e:
            print(e)
        finally:
            self.m_oss.umount()

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)
    def db(self,name):
        bg=time.time()
        try:
            self.m_oss.mount()

            conp=self.conp_ssh
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            suffix=self.get_suffix()
            user,password,ip,db,schema=self.conp
            arr=ip.split(":")
            host=arr[0]
            port='5432' if len(arr)==1 else arr[1]


            #(set PGPASSWORD=zhulong!123) & pg_dump -U developer -h 192.168.4.183 -d base_db -F c -v -t dm.qy_base -f
            file="%s/%s_db_%s.dmp"%(self.file_dir,self.app,name+'_'+suffix)
            if self.app  not in ['app5','gp']:
                cmd="export PGPASSWORD='%s' && %s/pg_dump  -U %s -h %s -p %s -d %s -F c -v  -f %s"%(password,self.pg_dump_dir,user,host,port,name,file)
                cmd1="export PGPASSWORD=*** && %s/pg_dump  -U %s -h %s -p %s -d %s -F c -v  -f %s"%(self.pg_dump_dir,user,host,port,name,file)
            else:
                cmd="""su -l %s -c "export PGPASSWORD='%s' && %s/pg_dump  -U %s -h %s -p %s -d %s -F c -v  -f %s" """%(self.superuser,password,self.pg_dump_dir,user,host,port,name,file)
                cmd1="export PGPASSWORD=*** && %s/pg_dump  -U %s -h %s -p %s -d %s -F c -v  -f %s"%(self.pg_dump_dir,user,host,port,name,file)
            print(cmd)
            c.run(cmd,pty=True)
        except Exception as e:
            print(e)
        finally:
            self.m_oss.umount()

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)

    def spec_app1(self):
        bg=time.time()
        try:
            self.m_oss.mount()

            conp=self.conp_ssh
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            suffix=self.get_suffix()
            user,password,ip,db,schema=self.conp
            arr=ip.split(":")
            host=arr[0]
            port='5432' if len(arr)==1 else arr[1]


            #(set PGPASSWORD=zhulong!123) & pg_dump -U developer -h 192.168.4.183 -d base_db -F c -v -t dm.qy_base -f
            file="%s/app1_%s.dmp"%(self.file_dir,suffix)

            cmd="export PGPASSWORD='%s' && %s/pg_dump  -U %s -h %s -p %s -d biaost -n public -T public.gg_html -F c -v  -f %s"%(password,self.pg_dump_dir,user,host,port,file)
            cmd1="export PGPASSWORD=*** && %s/pg_dump  -U %s -h %s -p %s -d biaost -n public -T public.gg_html -F c -v  -f %s"%(self.pg_dump_dir,user,host,port,file)
        
            print(cmd)
            c.run(cmd,pty=True)
        except Exception as e:
            print(e)
        finally:
            self.m_oss.umount()

        self.tb('public.gg_html')
        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)


    def web(self):
        bg=time.time()
        try:
            self.m_oss.mount()

            conp=self.conp_ssh
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            suffix=self.get_suffix()
            files=['apk','fileroot','tomcat','images']
            #files=['tomcat']
            for file in files:
                filename='%s_%s.tar.gz'%(file,suffix)
                if file!='fileroot':
                    cmd="tar cvf /jdoss/backup/web/%s /data/%s"%(filename,file)
                else:
                    cmd="tar cvf /jdoss/backup/web/%s /data/cloud-upload/%s"%(filename,file)
                print(cmd)

                c.run(cmd,pty=True)
        except Exception as e:
            print(e)
        finally:
            self.m_oss.umount()

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)


    def db4_get_databases(self):
        sql="select datname from pg_database where datname !~'postgres|template' order by datname "
        df=db_query(sql,dbtype="postgresql",conp=self.conp)
        arr=df['datname'].tolist()
        return arr 

    def db4_all(self):
        arr=self.db4_get_databases()
        for w in arr:print(w)
        for w in arr:
            #if w in ['anhui']:continue
            self.db(w)




    def test_result(self):

        result1="""backup(app='app5').tb('public.qy_zz')  128M cost  ---36 s """
        result2="""backup(app='app5').tb('public.qy_base')  1.2G cost  ---245 s  5M/s"""
        result3="""backup(app='app5').schema('cdc')  14M cost  ---127 s  """

        result4="""backup(app='app1').tb('public.wenshu')  7.5G cost  ---  2873 s """

        result6="""backup(app='app1').spec_app1()  8g+120g cost  ---  55500 s """

        result7="""backup(app='web').web()  1.7g cost  ---  127s """

        result8="""backup(app='app5').db('biaost')  43 cost  ---  7000s """

        result9="""backup(app='app5').db('biaost')  43 cost  ---  55500 """

    
    def strategy(self):
        pass 


def task_web_sys(loc='aliyun'):
    m=backup(loc=loc,app='web')
    m.web()

    m=backup(loc=loc,app='app1')
    
    m.spec_app1()

    m=backup(loc=loc,app='app5')
    m.db('biaost')

def task_gp_sys(loc='aliyun'):


        m=backup(app='gp')
        #m.db('biaost')
        # m.db('biaost')
        #m.mount()
        tbs=['dm.qy_zz','dm.qy_zcry','dm.t_zz','dm.t_person','dm.qy_base','dm.feiyan','dm.zlqy_t_qy_zhuce','dm.zizhi_t_zizhi'
        ,'dm.t_person_pre','dm.qyzz','dm.qyzcry','dm.t_qyzcry_result','dm.t_qyzz_result','dm.t_qyzcry','dm.t_qyzz']
        for tb in tbs:
            m.tb(tb)
        for sc in ['bid','src']:
            m.schema(sc)

def task_db4_sys(loc='aliyun'):
    def f(num):
        app='db%d'%num
        m=backup(loc=loc,app=app)
        m.db4_all()
    mythread(arr=[1,2,3,4],f=f).run(num=4)
#m.m_oss.umount()
# task_gp_sys()
def task():
    def f(num):
        if num==1:
            task_db4_sys()
        elif num==2:
            task_web_sys()
        elif num==3:
            task_gp_sys()
    mythread(arr=[1,2,3],f=f).run(3)

task()
# m=backup(app='db4')
# arr=m.db4_get_databases()
#m.pre_oss()
# m.db('hubei')
