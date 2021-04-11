from fabric import Connection
from invoke import Responder
import shutil
import os ,re
from lmfinstall import common
import sys ,time
from lmf.tool import down_file,mythread
import copy
import traceback 

class gp_ext:
    def __init__(self,pin=None):
        if pin is None:
            self.pin=[
                ["root@172.16.0.10:22","Since2015!","master"] ,
                ["root@172.16.0.11:22","Since2015!","seg1"] ,
                ["root@172.16.0.12:22","Since2015!","seg2"] ,
                ["root@172.16.32.6:22","Since2015!","seg3"] 
            ]
        else:
            self.pin=copy.deepcopy(pin)
        self.docker_file="D:\\webroot\\common\\greenplum-6.5\\plcontainer-python3-image-2.1.1-gp6.tar.gz"
        self.gpbackup_file="D:\\webroot\\common\\pivotal_greenplum_backup_restore-1.17.0-1-gp6-rhel-x86_64.gppkg"

    def plcontainer(self):
        cmds="""
            yum install -y yum-utils device-mapper-persistent-data lvm2
            yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            yum -y install docker-ce
            systemctl start docker
            usermod -aG docker gpadmin
            """
        cmds=re.sub('\n\s*','\n',cmds)
        cmds=cmds.split("\n")
        cmds=list(filter(lambda x:x.strip()!='',cmds))
        print(cmds)
        for cmd in cmds:
            print(cmd)
            self.ssh_run(cmd)

        conp=self.pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
            fpath=__file__ if __name__!='__main__' else sys.argv[0]
            for  f_name in os.listdir(os.path.join(os.path.dirname(fpath),'ext')):
                file=os.path.join(os.path.dirname(fpath),'ext',f_name)
                c.put(file,'/home/gpadmin')

            c.run("""su -l gpadmin -c "gppkg -i /home/gpadmin/plcontainer-2.1.1-gp6-rhel7_x86_64.gppkg" """)

    def plcontainer_prt1(self):
        sdir=self.docker_file
        tdir="/data/docker_file"
        file_dir,file_name=os.path.split(sdir)
        def f(conp):
            c=Connection(conp[0],connect_kwargs={"password":conp[1]}) 
            if c.run("test -f %s"%tdir,warn=True).failed:
                c.run("mkdir -p %s"%tdir)
            if  c.run("test -f %s/%s"%(tdir,file_name),pty=True,warn=True).failed:
                print("上传docker_file")
                c.put(sdir,tdir)
            else:
                print("上传docker_file")
                c.run("rm -rf  %s/%s"%(tdir,file_name))
                c.put(sdir,tdir)
                print("上传完成")
            c.run("""su -l gpadmin -c "docker load -i  %s/%s" """%(tdir,file_name))

        mythread(f=f,arr=self.pin).run(num=min(len(self.pin),5))
        conp=self.pin[0]
        asw1=Responder("Yy|Nn","y\n")
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:

            c.run("su -l gpadmin -c 'gpstop -M immediate' ",pty=True,watchers=[asw1])
            c.run("su -l gpadmin -c 'gpstart -a -B 15' ",pty=True)

    def plcontainer_prt1_oss(self):

        pass


    def gpbackup(self):
        sdir=self.gpbackup_file
        tdir="/data/gpext"
        file_dir,file_name=os.path.split(sdir)
        conp=self.pin[0]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]}) 
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
            c.run("chown gpadmin:gpadmin %s"%tdir)
        if  c.run("test -f %s/%s"%(tdir,file_name),pty=True,warn=True).failed:
            print("上传pgbackup安装包")
            c.put(sdir,tdir)
        else:
            print("上传pgbackup安装包")
            c.run("rm -rf  %s/%s"%(tdir,file_name))
            c.put(sdir,tdir)
            print("上传完成")
        c.run("""su -l gpadmin -c "gppkg -i  %s/%s" """%(tdir,file_name))

    def cgroup(self):
        def f(conp):
            c= Connection(conp[0],connect_kwargs={"password":conp[1]}) 
            c.run("hostname && yum install libcgroup-tools -y ")
            cmd="""
                group gpdb {
                     perm {
                         task {
                             uid = gpadmin;
                             gid = gpadmin;
                         }
                         admin {
                             uid = gpadmin;
                             gid = gpadmin;
                         }
                     }
                     cpu {
                     }
                     cpuacct {
                     }
                     cpuset {
                     }
                     memory {
                     }
                } 
            """
            cmd=cmd.replace("\n            ",'\n')
            cmd="echo '%s' > /etc/cgconfig.d/gpdb.conf"%cmd
            c.run(cmd)
            c.run("cgconfigparser -l /etc/cgconfig.d/gpdb.conf ",pty=True)
            c.run("systemctl enable cgconfig.service")
            c.run("systemctl restart cgconfig.service")
        mythread(f=f,arr=self.pin).run(int(len(self.pin)/3))
        conp=self.pin[0]
        c= Connection(conp[0],connect_kwargs={"password":conp[1]}) 
        cmd="""su -l gpadmin -c "gpconfig -c gp_resource_manager -v group" """
        print(cmd)
        c.run(cmd)

    def ssh_run(self,cmd):
        def f(conp):
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run(cmd,pty=True,warn=True)
        mythread(f=f,arr=self.pin).run(num=len(self.pin))


#gp_ext().cgroup()

#txt="""ssadad\nwwrwrwrw,"","ww",\n\r,""\n,"w"\r\n,"ww"\n\r    """