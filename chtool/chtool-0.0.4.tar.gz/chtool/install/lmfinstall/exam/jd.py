from lmfinstall.greenplum.v2.core import gp 
import time 
from lmfinstall.ambari.v1.core import ambari 
from lmf.tool import  mythread
from lmfinstall import common 
from lmfinstall.postgresql import postgresql1061
import copy
from fabric import Connection
from lmf.dbv2 import db_command_ext 
#20200616京东云从零部署
class jd_gp:
    def __init__(self):
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

        self.db_conp=['postgres','since2015','10.0.64.26','ambari','public']

        self.gp_file="D:\\迁移部署\\greenplum-db-6.5.0-rhel7-x86_64.rpm"
        self.python_file="D:\\迁移部署\\Python-3.5.2.tgz"
        self.java_file="D:\\迁移部署\\jdk-8u151-linux-x64.rpm"
        self.pg_file="D:\\迁移部署\\postgresql-10.6-1-linux-x64.run"

        self.repo_dict={"ambari":"http://10.0.64.25/repo/ambari-centos7-2.6.2.2/"
        ,"hdp":"http://10.0.64.25/repo/HDP-centos7-2.6.5.0/"
        ,"hdp_utils":"http://10.0.64.25/repo/HDP-UTILS-1.1.0.22-centos7/HDP-UTILS/centos7/1.1.0.22/"}

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

    #安装GP
    def gp_prt(self):
        self.gp_prt1()
    def gp_prt1(self):
        bg=time.time()
        m=gp(file=self.gp_file,pin=self.gp_pin)
        m.segs_pernode=3
        m.mirror=True
        m.pyver='3.5'
        m.data_prefix="/data/greenplum"
        m.standby_tag=True
        m.env_tag=False
        m.total_new(java_file=self.java_file,python_file=self.python_file)
        ed=time.time()
        cost=int(ed-bg)
        print("totally coast %d s"%cost)

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
        self.hdp_prt()
        self.gp_prt()
        ed=time.time()
        cost=int(ed-bg)
        print("base total--cost--%d s"%cost)

    def test(self):
        for conp in self.pin:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("hostname && ip addr")

# m=jd()
# m1=gp(file=m.gp_file,pin=m.gp_pin)
# m1.python(m.python_file)
#jd().base()
#jd().gp_prt()
#jd().os_prt()
#jd().gp_prt()

#jd().hdp_prt()