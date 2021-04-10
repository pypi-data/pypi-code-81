from lmfinstall.greenplum.v2.core import gp 
import time 
from lmfinstall.ambari.v1.core import ambari 
from lmf.tool import  mythread
from lmfinstall import common 
from lmfinstall.postgresql import postgresql1061
import copy
from fabric import Connection
from lmf.dbv2 import db_command_ext ,db_command,db_query
import shutil 
from zljd.core.oss import oss 
import os
#20200616京东云从零部署
class jd_gp:
    def __init__(self,local_file_download=True):
        self.pin=[
                    ['root@10.0.64.26:22','BST@2020610','metadb1'],
                    ['root@10.0.64.27:22','BST@2020610','metadb2'],
                    ['root@10.0.64.28:22','BST@2020610','master1'],
                    ['root@10.0.64.29:22','BST@2020610','master2'],
                    ['root@10.0.64.30:22','BST@2020610','master3'],
                    ['root@10.0.64.31:22','BST@2020610','master4'],
                    ['root@10.0.64.32:22','BST@2020610','datanode1'],
                    ['root@10.0.64.33:22','BST@2020610','datanode2'],
                    ['root@10.0.64.34:22','BST@2020610','datanode3'],
                    ['root@10.0.64.35:22','BST@2020610','datanode4'],
                    ['root@10.0.64.36:22','BST@2020610','datanode5'],
                    ['root@10.0.64.37:22','BST@2020610','datanode6'],
                    ['root@10.0.64.38:22','BST@2020610','datanode7'],
                    ['root@10.0.64.39:22','BST@2020610','datanode8'],
                    ['root@10.0.64.40:22','BST@2020610','datanode9'],
                    ['root@10.0.64.41:22','BST@2020610','datanode10'],
                    ['root@10.0.64.42:22','BST@2020610','datanode11'],
                    ['root@10.0.64.43:22','BST@2020610','datanode12'],
                    ['root@10.0.64.44:22','BST@2020610','datanode13'],
                    ['root@10.0.64.45:22','BST@2020610','datanode14'],
                    ['root@10.0.64.46:22','BST@2020610','datanode15'],




                    ]
        self.hdp_pin=self.get_pin(range(2,21))

        self.gp_pin=self.get_pin([4,*range(6,21),5])

        self.pg_master,self.pg_slave=self.get_pin([0,1])
        ip=self.pg_master[0]
        ip=ip[ip.index("@")+1:ip.index(":")]

        self.db_conp=['postgres','since2015',ip,'ambari','public']
        self.gp_oss_date='20200629'

        self.oss_internal=True
        self.local_file_dir="D:\\jingdong_gpsys_download"
        self.local_file_download=local_file_download 
        self.init_local_file()
        self.init_oss_file()

        self.repo_dict={"ambari":"http://10.0.64.25/repo/ambari-centos7-2.6.2.2/"
        ,"hdp":"http://10.0.64.25/repo/HDP-centos7-2.6.5.0/"
        ,"hdp_utils":"http://10.0.64.25/repo/HDP-UTILS-1.1.0.22-centos7/HDP-UTILS/centos7/1.1.0.22/"}

    def init_oss_file(self):
        self.gp_data_files=[]
        for name in [
        'gp_tb_dm.qy_base',
        'gp_tb_dm.qy_zz',
        'gp_schema_bid',
        'gp_tb_dm.qy_zcry',
        'gp_schema_src',
        'gp_tb_dm.t_person'
        ]:
            file="/jdoss/backup/gp/%s_%s.dmp"%(name,self.gp_oss_date)
            self.gp_data_files.append(file)

    def init_local_file(self):
        tmpdir=self.local_file_dir

        self.gp_file="%s\\greenplum-db-6.5.0-rhel7-x86_64.rpm"%tmpdir
        self.java_file="%s\\jdk-8u151-linux-x64.rpm"%tmpdir
        self.pg_file="%s\\postgresql-10.6-1-linux-x64.run"%tmpdir
        self.python_file="%s\\Python-3.5.2.tgz"%tmpdir


    def down_gpfile(self):
        tmpdir=self.local_file_dir
        if self.local_file_download:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            files=['Python-3.5.2.tgz', 
            'greenplum-db-6.5.0-rhel7-x86_64.rpm', 'jdk-8u151-linux-x64.rpm', 'postgresql-10.6-1-linux-x64.run']
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

    def get_pin(self,arr):
        p=[]
        for i in arr:
            p.append(copy.deepcopy(self.pin[i]))
        return p 

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
        k1='/dev/vdc'
        v1='/data1'
        for conp in self.pin :
            print(conp[2])
            if 'datanode' not in conp[2]:
                common.mount(conp,k,v)
            else:
                common.mount(conp,k,v)
                common.mount(conp,k1,v1)
    def test(self):   
        for conp in self.pin:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("hostname && ip addr")


    #安装GP
    def gp_prt(self):
        self.test()
        self.down_gpfile()
        self.gp_prt1()
        self.gp_prt2()
        self.gp_prt3()
        self.gp_prt4()
    def gp_prt1(self):
        bg=time.time()
        m=gp(file=self.gp_file,pin=self.gp_pin)
        m.segs_pernode=3
        m.mirror=False
        m.pyver='3.5'
        m.data_prefix="/data/greenplum"
        m.standby_tag=True
        m.env_tag=False
        m.total_new(java_file=self.java_file,python_file=self.python_file)
        ed=time.time()
        cost=int(ed-bg)
        print("totally coast %d s"%cost)


    def gp_prt2(self):
        #创建角色
        mconp=self.gp_pin[1]
        print(mconp)
        c=Connection(mconp[0],connect_kwargs={"password":mconp[1]})
        c.run("hostname && ip addr",pty=True)
        c.run("for i in {1..15};do ssh datanode$i 'mkdir -p /data1/greenplum && chown gpadmin:gpadmin /data1/greenplum';done ",pty=True,warn=True)
        c.run("ssh master3 'mkdir -p /data1/greenplum && chown gpadmin:gpadmin /data1/greenplum' ",pty=True,warn=True)
        c.run(" ssh master4 'mkdir -p /data1/greenplum && chown gpadmin:gpadmin /data1/greenplum' ",pty=True,warn=True)
        ip=self.gp_pin[0][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        sql="create database base_db;"
        db_command_ext(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])
        sql="create schema dm;"
        db_command_ext(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])


        extension=['plpython3u','pgcrypto','dblink','pxf']
        for ext in extension:
            sql="create extension  if not exists %s"%ext
            print(sql)
            db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])

        schemas=['cdc']
        for schema in schemas:
            sql="create schema  if not exists %s"%ext
            print(sql)
            db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])

        for user in ['app_reader','zl_reader']:
            sql1="create user app_reader with password 'app_reader';"
            sql2="grant usage on schema public to app_reader;"
            sql3="grant select on all tables in schema public to app_reader;"
            sql=sql1+sql2+sql3
            sql=sql.replace('app_reader',user)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])

        sql="create user developer with superuser password 'zhulong!123' "

        print(sql)
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])

        sql="create tablespace bst_file location '/data1/greenplum' "
        db_command_ext(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'base_db','public'])

    def gp_prt3(self):
        conp=self.gp_pin[0]
        m=oss(conp=conp)
        m.s3fs_pre()

    def gp_prt4(self):
        for file in self.gp_data_files:
            self.gp_prt4_restore_file(file)
    def gp_prt4_restore_file_2(self,filename):

        #rs=restore(loc='jdyun',app='gp')
        pass


    def gp_prt4_restore_file(self,filename):
        conp=self.gp_pin[0]
        m_oss=oss(conp=conp)


        bg=time.time()
        ip=conp[0]
        ip=ip[ip.index('@')+1:ip.index(':')]

        gp,filetype,name=filename.split("_",2)
        #name=re.
        try:
            m_oss.mount()
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            cmd="su -l gpadmin -c 'pg_restore -d base_db -U gpadmin -d base_db -v   %s' "%filename
            print(cmd)
            c.run(cmd,warn=True)
            

        except Exception as e:
            print(e)
        finally:
            m_oss.umount()
            print("umount")

        ed=time.time()
        cost=int(ed-bg)
        print("恢复%s -  %s %s  耗时 %d s "%(gp,filetype,filename,cost))
    def hdp_prt(self):
        self.hdp_prt1()
        self.hdp_prt2()

    #元数据库主从
    def hdp_prt1(self):
        conp1,conp2=self.pg_master,self.pg_slave
        postgresql1061.install(conp1,self.pg_file,pgdata="/data/postgresql")
        postgresql1061.install(conp2,self.pg_file,pgdata="/data/postgresql")
        postgresql1061.master_slave(conp1,conp2,"/data/postgresql","/data/postgresql")


    #ambari安装
    def hdp_prt2(self):
        sql1="create database hive;"
        sql2="create database ambari;"
        print(sql1,sql2)
        conp=copy.deepcopy(self.db_conp)
        conp[3]='postgres'
        db_command_ext(sql1,dbtype="postgresql",conp=conp)
        db_command_ext(sql2,dbtype="postgresql",conp=conp)
        #conp_master=self.pg_master

        repo_dict=self.repo_dict
        conp=self.db_conp
        m=ambari(repo_dict=repo_dict,conp=conp,pin=self.hdp_pin)
        m.env_tag=False
        m.from_zero(java_file=self.java_file)
        print("hadoop  jar /usr/hdp/2.6.5.0-292/hadoop-mapreduce/hadoop-mapreduce-examples.jar  pi 10 10")


    def base(self):
        self.test()
        bg=time.time()
        self.os_prt()
        self.gp_prt()
        self.hdp_prt()

        ed=time.time()
        cost=int(ed-bg)
        print("base total--cost--%d s"%cost)

    def test(self):
        for conp in self.pin:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("hostname && ip addr")


class jd_gp_exam(jd_gp):
    def __init__(self,local_file_download=True):
        super().__init__(local_file_download=local_file_download)
        self.pin=[
                    ['root@10.0.64.26:22','BST@dw2020610','metadb1'],
                    ['root@10.0.64.27:22','BST@dw2020610','metadb2'],
                    ['root@10.0.64.28:22','BST@dw2020610','master1'],
                    ['root@10.0.64.29:22','BST@dw2020610','master2'],
                    ['root@10.0.64.30:22','BST@dw2020610','master3'],
                    ['root@10.0.64.31:22','BST@dw2020610','master4'],
                    ['root@10.0.64.32:22','BST@dw2020610','datanode1'],
                    ['root@10.0.64.33:22','BST@dw2020610','datanode2'],
                    ['root@10.0.64.34:22','BST@dw2020610','datanode3'],
                    ['root@10.0.64.35:22','BST@dw2020610','datanode4'],
                    ['root@10.0.64.36:22','BST@dw2020610','datanode5'],
                    ['root@10.0.64.37:22','BST@dw2020610','datanode6'],
                    ['root@10.0.64.38:22','BST@dw2020610','datanode7'],
                    ['root@10.0.64.39:22','BST@dw2020610','datanode8'],
                    ['root@10.0.64.40:22','BST@dw2020610','datanode9'],
                    ['root@10.0.64.41:22','BST@dw2020610','datanode10'],
                    ['root@10.0.64.42:22','BST@dw2020610','datanode11'],
                    ['root@10.0.64.43:22','BST@dw2020610','datanode12'],
                    ['root@10.0.64.44:22','BST@dw2020610','datanode13'],
                    ['root@10.0.64.45:22','BST@dw2020610','datanode14'],
                    ['root@10.0.64.46:22','BST@dw2020610','datanode15'],




                    ]
        self.hdp_pin=self.get_pin(range(2,21))

        self.gp_pin=self.get_pin([4,*range(6,21),5])

        self.pg_master,self.pg_slave=self.get_pin([0,1])
        ip=self.pg_master[0]
        ip=ip[ip.index("@")+1:ip.index(":")]

        self.db_conp=['postgres','since2015',ip,'ambari','public']
        self.gp_oss_date='20200630'

        self.oss_internal=True
        self.local_file_dir="D:\\jingdong_gpsys_download"
        self.local_file_download=local_file_download 
        self.init_local_file()
        self.init_oss_file()
        self.gp_data_files=[]

        self.repo_dict={"ambari":"http://10.0.64.25/repo/ambari-centos7-2.6.2.2/"
        ,"hdp":"http://10.0.64.25/repo/HDP-centos7-2.6.5.0/"
        ,"hdp_utils":"http://10.0.64.25/repo/HDP-UTILS-1.1.0.22-centos7/HDP-UTILS/centos7/1.1.0.22/"}

    def task(self):
        bg=time.time()


        self.test()
        self.os_prt()
        self.gp_prt()
        self.hdp_prt()


        ed=time.time()
        cost=int(ed-bg)
        #60000s
        print("totally--cost %d s"%cost)

def task1():
    from zljd.core.sdk import sdk 
    sdk().rebuild_hosts('gp_dw')
    m=jd_gp_exam(True)
    m.task()

if __name__=='__main__':
    ##3228s
    #task1()
    pass
    # m=jd_gp_exam(False)
    # m.gp_prt2()