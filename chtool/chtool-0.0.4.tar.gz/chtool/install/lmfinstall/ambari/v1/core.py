from fabric import Connection
from invoke import Responder
import time
from lmfinstall import common
from lmf.tool import mythread ,down_file
import os ,sys,copy
import re 


class ambari:
    def __init__(self,repo_dict,conp,pin=None):
        if pin is None:
            self.pin=[
                ["root@172.16.0.10:22","Since2015!","master"] ,
                ["root@172.16.0.11:22","Since2015!","seg1"] ,
                ["root@172.16.0.12:22","Since2015!","seg2"] ,
                ["root@172.16.32.6:22","Since2015!","seg3"] 
            ]
        else:
            self.pin=copy.deepcopy(pin)

        self.repo_dict=copy.deepcopy(repo_dict)
        self.ambari_conp=copy.deepcopy(conp)
        self.env_tag=True

    def from_zero(self,java_file=None):
        """
        self.base()
        if java_file is None:
            java_file="None:jdk-8u151-linux-x64.rpm"
        java_file=self.download(java_file)
        self.java(java_file)

        self.repo(self.repo_dict)

        self.ambsrv()

        self.ambari_ist()
        """
        if self.env_tag:self.base()

        if java_file is None:
            java_file="None:jdk-8u151-linux-x64.rpm"
        java_file=self.download(java_file)
        self.java(java_file)

        self.repo()

        self.ambsrv()

        self.ambari_ist()


    def base(self):

        common.hostname(self.pin)

        common.dns(self.pin)

        common.ssh(self.pin)

    def download(self,gprpm_file):
        bg=time.time()
        if not os.path.exists('/tmp') :os.mkdir("/tmp")
        path="/tmp"
        if gprpm_file.startswith("None"):
            w1,w2=gprpm_file.split(":")
            gprpm_file1="http://106.13.239.200/common/"+w2
        elif gprpm_file.startswith("local") :
            w1,w2=gprpm_file.split(":")
            gprpm_file1="http://127.0.0.1/common/"+w2
        elif gprpm_file.startswith("http") :
            gprpm_file1=gprpm_file
            w1,w2=gprpm_file.split(":")
        else:
            gprpm_file1=gprpm_file
            return gprpm_file1
        
        filename=os.path.join(path,os.path.split(gprpm_file1)[1])
        print(gprpm_file1,filename)
        tag=down_file(gprpm_file1,filename)
        ed=time.time()
        cost=int(ed-bg)
        print("cost---%d s"%cost)
        if tag :
            return filename
        else:
            return tag

    def java(self,java_file):
        arr=copy.deepcopy(self.pin)
        f=lambda conp:common.java(conp,java_file)
        mythread(arr,f).run(num=min(5,len(arr)))

    def repo(self):
        repo_dict=self.repo_dict

        repo1="""
            [ambari]
            name=ambari
            baseurl=http://172.16.0.25/ambari/2.5.0.3/centos7/
            enabled=1
            gpgcheck=0
            """
        repo2="""
            [hdp]
            name=hdp.repo 

            baseurl=http://172.16.0.25/HDP/2.6.0/centos7/

            enabled=1

            gpgcheck=0

            [hdp_utils]
            name=hdp hdp_utils 

            baseurl=http://172.16.0.25/HDP-UTILS-1.1.0.21-centos7/

            enabled=1
            gpgcheck=0

            [hawq-repo]
            name=hawq-repo 
            baseurl=http://172.16.0.25/HAWQ/hawq_rpm_packages/
            enabled=0
            gpgcheck=0
        """
        repo1=re.sub('\n\s*','\n',repo1)
        repo2=re.sub('\n\s*','\n',repo2)
        if "ambari" in repo_dict.keys():
            repo1=repo1.replace("http://172.16.0.25/ambari/2.5.0.3/centos7/",repo_dict["ambari"])
        else:
            repo1=re.sub('\[ambari\][.\n\s\S]*?(?!=\[)','',repo1)

        if "hdp" in repo_dict.keys():
            repo2=repo2.replace("http://172.16.0.25/HDP/2.6.0/centos7/",repo_dict["hdp"])
        else:
            repo2=re.sub('\[hdp\][.\n\s\S]*?(?=\[)','',repo2)
        if "hdp_utils" in repo_dict.keys():
            repo2=repo2.replace("http://172.16.0.25/HDP-UTILS-1.1.0.21-centos7/",repo_dict["hdp_utils"])
        else:
            repo2=re.sub('\[hdp_utils\][.\n\s\S]*?(?=\[)','',repo2)

        if "hawq" in repo_dict.keys():
            repo2=repo2.replace("http://172.16.0.25/HAWQ/hawq_rpm_packages/",repo_dict["hawq"])
        else:
            repo2=re.sub('\[hawq-repo\][.\n\s\S]*','',repo2)


        for conp in self.pin:

            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            c.run("""echo "%s" > /etc/yum.repos.d/ambari.repo"""%repo1,pty=True)

            c.run("""echo "%s" > /etc/yum.repos.d/hdp.repo"""%repo2,pty=True)



    def ambsrv(self):
        pin=copy.deepcopy(self.pin)
        def f1(conp):
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("yum install ambari-agent -y",pty=True)
        mythread(pin,f1).run(min(4,len(pin)))
        for conp in pin :
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            if conp[0]==pin[0][0]:
                c.run("yum install ambari-server -y",pty=True)
            c.run("sed -i '/force_https_protocol=/d' /etc/ambari-agent/conf/ambari-agent.ini")
            c.run("sed -i '/\[security\]/a force_https_protocol=PROTOCOL_TLSv1_2'  /etc/ambari-agent/conf/ambari-agent.ini")
            c.run("sed -i 's/verify=platform_default/verify=disable/g'   /etc/python/cert-verification.cfg")


    def ambari_ist(self):
        master_conp=self.pin[0]
        ambari_conp=self.ambari_conp
        c=Connection(master_conp[0],connect_kwargs={"password":master_conp[1]})

        amasw0=Responder("Customize user account for ambari-server","y\n")
        amasw1=Responder("Enter user account for ambari-server daemon","\n")
        amasw2=Responder("JDK.{,100}Enter choice","3\n")
        amasw3=Responder("Path to JAVA_HOME","/usr/java/jdk1.8.0_151\n")
        amasw4=Responder("Enable Ambari Server to download and install GPL Licensed LZO packages","n\n")
        amasw5=Responder("Enter advanced database configuration","y\n")
        amasw6=Responder("BDB.{,100}Enter choice","4\n")
        amasw7=Responder("Hostname","%s\n"%ambari_conp[2])
        amasw8=Responder("Port","\n")
        amasw9=Responder("Database name","\n")
        amasw10=Responder("Postgres schema","%s\n"%ambari_conp[4])
        amasw11=Responder("Username","%s\n"%ambari_conp[0])
        amasw12=Responder("Enter Database Password","%s\n"%ambari_conp[1])
        amasw13=Responder("Re-enter password","%s\n"%ambari_conp[1])
        amasw14=Responder("Proceed with configuring remote database connection properties","y\n")
        c.run("ambari-server setup",pty=True,watchers=[amasw0,amasw1,amasw2,amasw3,amasw4,amasw5,amasw6,amasw7,amasw8,amasw9,amasw10,amasw11,amasw12,amasw13,amasw14])

        c.run("/usr/bin/psql -U %s -h %s -d %s -f /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql"%(ambari_conp[0],ambari_conp[2],ambari_conp[3]),pty=True,watchers=[Responder("Password for user","%s\n"%ambari_conp[1])])
        c.run("ambari-server start",pty=True)


        if c.run("test -f /root/postgresql-42.2.1.jar",warn=True).failed:
            print("上传postgresql-42.2.1.jar")
            if __name__!='__main__':
                path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','postgresql-42.2.1.jar')
            else:
                path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))),'data','postgresql-42.2.1.jar')
            c.put("%s"%path,r"/root")
        c.run("ambari-server setup --jdbc-db=postgres --jdbc-driver=/root/postgresql-42.2.1.jar",pty=True)

