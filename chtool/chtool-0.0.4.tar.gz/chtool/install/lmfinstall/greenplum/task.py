from lmfinstall.greenplum.v2.core import gp 
import time 
from lmfinstall.ambari.v1.core import ambari 
def task1():
    #800s
    bg=time.time()
    m=gp(file="local:greenplum-db-6.5.0-rhel7-x86_64.rpm")
    m.total_new(java_file="local:jdk-8u151-linux-x64.rpm",python_file="local:Python-3.5.2.tgz")

    ed=time.time()
    cost=int(ed-bg)
    print("totally coast %d s"%cost)
        #m.python(python_file="D:/tmp/Python-3.5.2.tgz")



def task2():
    pin=[
                ["root@172.16.0.10:22","Since2015!","master"] ,
                ["root@172.16.0.11:22","Since2015!","seg1"] ,
                ["root@172.16.0.12:22","Since2015!","seg2"] ,
                ["root@172.16.32.6:22","Since2015!","seg3"] 
            ]
    repo_dict={"ambari":"http://172.16.0.9/repo/ambari-centos7-2.6.2.2/"
    ,"hdp":"http://172.16.0.9/repo/HDP-centos7-2.6.5.0/"
    ,"hdp_utils":"http://172.16.0.9/repo/HDP-UTILS-1.1.0.22-centos7/HDP-UTILS/centos7/1.1.0.22/"}

    conp=["postgres",'since2015','172.16.0.9','ambari','public']
    m=ambari(repo_dict=repo_dict,conp=conp,pin=pin)
    m.from_zero(java_file="local:jdk-8u151-linux-x64.rpm")
    print("hadoop  jar /usr/hdp/2.6.5.0-292/hadoop-mapreduce/hadoop-mapreduce-examples.jar  pi 10 10")



task1()