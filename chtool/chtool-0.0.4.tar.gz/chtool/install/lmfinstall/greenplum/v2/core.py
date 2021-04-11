from fabric import Connection
from invoke import Responder
import shutil
import os ,re
from lmfinstall import common
import sys ,time
from lmf.tool import down_file,mythread
import copy
import traceback 
# 整个设计，前提是，soft只有一份
# 2019-10-08  支持为非gpadmin 用户一步安装
#
#2019-10-08  支持  动态重启 data  和  增加新用户 
# greenplum-db-6.0.0-beta.6-rhel7-x86_64.rpm 
#需要一个下载工具
class gp:

    def __init__(self,file=None,pin=None):
        """
        file  file 搜寻本地
        file  None 
        file  local:greenplum-db-6.5.0-rhel7-x86_64.rpm 
        file  http://..greenplum-db-6.5.0-rhel7-x86_64.rpm
        file  None:greenplum-db-6.5.0-rhel7-x86_64.rpm
        http://106.13.239.200/common/greenplum-db-6.5.0-rhel7-x86_64.rpm
        self.tpath="/root"
        self.superuser="gpadmin"
        self.segs_pernode=3
        self.data_prefix="/data/greenplum"
        self.init=True
        self.mirror=True
        self.standby_tag=False
        self.pyver='3.5'
        """
        if pin is None:
            self.pin=[
                ["root@172.16.0.10:22","Since2015!","master"] ,
                ["root@172.16.0.11:22","Since2015!","seg1"] ,
                ["root@172.16.0.12:22","Since2015!","seg2"] ,
                ["root@172.16.32.6:22","Since2015!","seg3"] 
            ]
        else:
            self.pin=copy.deepcopy(pin)
        if file is None:
            file="None:greenplum-db-6.5.0-rhel7-x86_64.rpm"

        file=self.download(file)
        self.gprpm_file=file

        self.tpath="/root"
        self.superuser="gpadmin"
        self.segs_pernode=3
        self.data_prefix="/data/greenplum"
        self.init=True
        self.mirror=True
        self.standby_tag=False
        self.pyver='3.5'
        self.env_tag=True
        if not self.standby_tag:
            print("standby 可以后加  gpinitstandby -s seg2 (seg2 上master 目录准备好 ,gpadmin-ssh 准备好 软件安装好)")


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


    def from_zero(self):
        if self.env_tag:self.pre_env()
        self.pre_cfg()
        self.soft()
        self.data()
        self.plpython3u(self.pyver)

    def total_new(self,python_file=None,java_file=None):
        self.from_zero()
        if python_file is None:
            python_file="None:Python-3.5.2.tgz"
        python_file=self.download(python_file)
        if java_file is None:
            java_file="None:jdk-8u151-linux-x64.rpm"
        java_file=self.download(java_file)

        self.python(python_file)
        self.java(java_file)
        self.pxf()

    def pxf(self):
        pin=self.pin
        superuser=self.superuser
        if __name__!='__main__':
            jar_file=os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,'data',"postgresql-42.2.1.jar" )
        else:
            jar_file=os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))) ,'data',"postgresql-42.2.1.jar" )
        print(jar_file)
        for w in pin:
            with Connection(w[0],connect_kwargs={"password":w[1],"banner_timeout":120}) as c:
                c.run("""rm -rf /usr/local/greenplum-db/pxf/pxf-service""")
                if c.run("test -f /usr/local/greenplum-db/pxf/lib/postgresql-42.2.1.jar",warn=True).failed:
                    print("上传postgresql-42.2.1.jar")
                    c.put(jar_file,r"/usr/local/greenplum-db/pxf/lib")
        for w in pin[:1]:
            with Connection(w[0],connect_kwargs={"password":w[1],"banner_timeout":120}) as c:
                c.run("""su %s -c "sed -i '/PXF_CONF/d' /home/%s/.bashrc " """%(superuser,superuser),pty=True)
                c.run("""su %s -c "echo 'export PXF_CONF=/home/%s/pxf' >> /home/gpadmin/.bashrc" """%(superuser,superuser),pty=True)
                c.run(""" su %s -c "source /home/%s/.bashrc && /usr/local/greenplum-db/pxf/bin/pxf cluster init && /usr/local/greenplum-db/pxf/bin/pxf cluster start  " """%(superuser,superuser))

    def plpython3u(self,ver='3.5'):
        pin,superuser=self.pin,self.superuser
        conp=pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
            fpath=__file__ if __name__!='__main__' else sys.argv[0]
            for  f_name in os.listdir(os.path.join(os.path.dirname(fpath),'gpplpython%s'%ver)):
                file=os.path.join(os.path.dirname(fpath),'gpplpython%s'%ver,f_name)
                c.put(file,'/root/')
            for conp in pin:
                c.run("scp /root/plpython3u* root@%s:/usr/local/greenplum-db/share/postgresql/extension/"%(conp[2]),pty=True,encoding='utf8')
                c.run("scp /root/plpython3.so root@%s:/usr/local/greenplum-db/lib/postgresql/"%(conp[2]),pty=True,encoding='utf8')
                c.run("ssh %s chown -R %s:%s /usr/local/greenplum-db*"%(conp[2],superuser,superuser),pty=True,encoding='utf8')
            c.clear()

    def extension(self,extension_name,ver=''):
        pin,superuser=self.pin,self.superuser
        conp=pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
            fpath=__file__ if __name__!='__main__' else sys.argv[0]
            for  f_name in os.listdir(os.path.join(os.path.dirname(fpath),'%s%s'%(extension_name,ver))):
                file=os.path.join(os.path.dirname(fpath),'%s%s'%(extension_name,ver),f_name)
                c.put(file,'/root/')
            for conp in pin:
                c.run("scp /root/%s*sql /root/%s*control root@%s:/usr/local/greenplum-db/share/postgresql/extension/"%(extension_name,extension_name,conp[2]),pty=True,encoding='utf8')
                c.run("scp /root/%s*so root@%s:/usr/local/greenplum-db/lib/postgresql/"%(extension_name,conp[2]),pty=True,encoding='utf8')
                c.run("ssh %s chown -R %s:%s /usr/local/greenplum-db*"%(conp[2],superuser,superuser),pty=True,encoding='utf8')
            c.clear()
    
    def python(self,python_file):
        from lmfinstall.python.python import install 
        arr=copy.deepcopy(self.pin)
        def f(conp):
            try:
                install(conp,python_file)
            except:
                traceback.print_exc()
        mythread(arr,f).run(num=min(5,len(arr)))
    def java(self,java_file):
        from lmfinstall.common import java 
        arr=copy.deepcopy(self.pin)
        f=lambda conp:java(conp,java_file)
        mythread(arr,f).run(num=min(5,len(arr)))

    def soft(self):
        superuser=self.superuser
        gprpm_file=self.gprpm_file

        pin=self.pin
        conp=self.pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
            sdir=gprpm_file
            tdir=self.tpath
            file_dir,file_name=os.path.split(sdir)
            if c.run("test -f %s"%tdir,warn=True).failed:
                c.run("mkdir -p %s"%tdir)
            if  c.run("test -f %s/%s"%(tdir,file_name),pty=True,warn=True).failed:
                print("上传greenplum rpm")
                c.put(sdir,tdir)
            for conp in pin:
                c.run("scp %s/%s root@%s:%s "%(tdir,file_name,conp[2],tdir),pty=True)
            c.clear()

        for conp in pin:
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
                if c.run("""egrep "^%s:" /etc/passwd"""%superuser,warn=True,pty=True).failed:

                    c.run("useradd  %s "%superuser,pty=True)

                c.run("passwd %s"%superuser,pty=True,watchers=[Responder("password|密码","since2015\n")],encoding='utf8')

                c.run("yum install -y  epel-release  wget cmake3 git gcc gcc-c++ bison flex libedit-devel zlib zlib-devel perl-devel perl-ExtUtils-Embed",pty=True,encoding='utf8',warn=True)

                c.run("yum install -y libcurl-devel bzip2 bzip2-devel net-tools libffi-devel openssl-devel",pty=True,encoding='utf8',warn=True)
                c.run("""yum  install -y  libevent libevent-devel libxml2 libxml2-devel """,pty=True,encoding='utf8',warn=True)

                c.run("yum install -y  epel-release  wget cmake3 git gcc gcc-c++ bison flex libedit-devel zlib zlib-devel perl-devel perl-ExtUtils-Embed",pty=True,encoding='utf8',warn=True)

                c.run("yum install -y libcurl-devel bzip2 bzip2-devel net-tools libffi-devel openssl-devel",pty=True,encoding='utf8',warn=True)
                c.run("""yum  install -y  libevent libevent-devel libxml2 libxml2-devel """,pty=True,encoding='utf8',warn=True)


                c.run("mkdir -p  /data/greenplum",pty=True,encoding='utf8')
                c.run("chown -R %s: /data/greenplum"%superuser,encoding='utf8')
                c.clear()
        for conp in pin:
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
                c.run("yum install -y  %s/%s"%(tdir,file_name),warn=True,encoding='utf8')
                #c.run("chown -R gpadmin:gpadmin /usr/local/greenplum-db",pty=True)
                c.run("chown -R %s:%s /usr/local/greenplum-db*"%(superuser,superuser),pty=True,encoding='utf8')
                c.clear()

    def data(self):
        superuser=self.superuser
        data_prefix=self.data_prefix
        segs_pernode=self.segs_pernode
        init=self.init
        mirror=self.mirror
        pin=self.pin

        standby=pin[-1][2]

        for conp in pin:
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c:
                if c.run("""egrep "^%s:" /etc/passwd"""%superuser,warn=True,pty=True).failed:
                    c.run("useradd  %s "%superuser,pty=True)
                c.run("passwd %s"%superuser,pty=True,watchers=[Responder("password|密码","since2015\n")],encoding='utf8')
                c.clear()
        all_nodes=[ conp[2] for conp in pin ]
        if not self.standby_tag :
            seg_nodes=all_nodes[1:]
        else:
            seg_nodes=all_nodes[1:-1]
        conp=pin[0]

        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120})  as c:
            c.sudo("sed -i /MASTER_DATA_DIRECTORY/d /home/%s/.bashrc  "%superuser,user=superuser ,encoding='utf8')
            c.sudo("sed -i /greenplum_path.sh/d /home/%s/.bashrc  "%superuser,user=superuser ,encoding='utf8')
            c.sudo("""cat >> /home/%s/.bashrc << EOF\nexport MASTER_DATA_DIRECTORY=%s/master/seg-1\nsource /usr/local/greenplum-db/greenplum_path.sh\nEOF"""%(superuser,data_prefix),user=superuser,encoding='utf8')
            c.clear()

        common.ssh(pin,superuser)

        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120})  as c:
            c.run("""su %s -c "echo '%s' > /home/%s/seg_nodes "  """%(superuser,"\n".join(seg_nodes),superuser) ,pty=True,encoding='utf8')
    
            c.run("""mkdir -p %s/master"""%data_prefix,encoding='utf8')
            c.run("""rm -rf %s/master/*"""%data_prefix,encoding='utf8')
            c.clear()
        #所有机器的data_prefix
        for conp in pin:
            with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c1:
                c1.run("""mkdir -p %s"""%data_prefix,encoding='utf8')

                c1.run("chown -R %s:%s %s "%(superuser,superuser,data_prefix),encoding='utf8')
                c1.clear()
        conp=pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120}) as c2:
            c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -h %s -e 'mkdir -p %s/master' " """%(superuser,superuser,standby,data_prefix),pty=True,encoding='utf8')
            c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -h %s -e 'rm -rf %s/master/*' " """%(superuser,superuser,standby,data_prefix),pty=True,encoding='utf8')
            c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -f /home/%s/seg_nodes -e 'mkdir -p %s/datap{1..%d}' " """%(superuser,superuser,superuser,data_prefix,segs_pernode),pty=True)
            c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -f /home/%s/seg_nodes -e 'mkdir -p %s/datam{1..%d}' " """%(superuser,superuser,superuser,data_prefix,segs_pernode),pty=True)
            c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -f /home/%s/seg_nodes -e 'rm -rf %s/data*/*' " """%(superuser,superuser,superuser,data_prefix),pty=True)
            if not mirror:
                c2.run("""su %s -c   " source /home/%s/.bashrc && gpssh -f /home/%s/seg_nodes -e 'rm -rf %s/datam{1..%d}' " """%(superuser,superuser,superuser,data_prefix,segs_pernode),pty=True)
            c2.clear()
        cmd="""cat > /home/%s/gpinitsystem_config << EOF
                    ARRAY_NAME="GREENPLUM-LMF"
                    SEG_PREFIX=seg
                    PORT_BASE=40000
                    MASTER_MAX_CONNECT=100
                    declare -a DATA_DIRECTORY=(/data/greenplum/data/datap1)
                    MASTER_HOSTNAME=mdw
                    MASTER_DIRECTORY=%s/master
                    MASTER_PORT=5432
                    TRUSTED_SHELL=ssh
                    ENCODING=UNICODE
                    MIRROR_PORT_BASE=50000
                    REPLICATION_PORT_BASE=41000
                    MIRROR_REPLICATION_PORT_BASE=51000
                    declare -a MIRROR_DATA_DIRECTORY=(/data/greenplum/data/datam1)
                    DATABASE_NAME=testdb
                    ENCODING=UTF-8
                    MACHINE_LIST_FILE=/home/%s/seg_nodes
                    EOF"""%(superuser,data_prefix,superuser)

        p="%s/datap{1..%d}"%(data_prefix,segs_pernode)
        m="%s/datam{1..%d}"%(data_prefix,segs_pernode)
        cmd=cmd.replace("/data/greenplum/data/datap1",p)
        cmd=cmd.replace("/data/greenplum/data/datam1",m)
        cmd=cmd.replace("MASTER_HOSTNAME=mdw","MASTER_HOSTNAME=%s"%pin[0][2])
        conp=pin[0]
        cmd=re.sub('\n\s*','\n',cmd)
        with Connection(conp[0],connect_kwargs={"password":conp[1],"banner_timeout":120})  as c:
            c.sudo(cmd,user=superuser,encoding='utf8')
            if not mirror:
                c.run("sed -i /MIRROR/d  /home/%s/gpinitsystem_config "%superuser,encoding='utf8')
            c.run("chown -R %s: /home/%s/gpinitsystem_config"%(superuser,superuser),encoding='utf8')
            if self.standby_tag :
                standby_str='-s %s'%standby
            else:
                standby_str=''
            if init:
                c.run("""su -l %s -c "source /home/%s/.bashrc && gpinitsystem -a -c /home/%s/gpinitsystem_config --su_password=since2015 %s" """%(superuser,superuser,superuser,standby_str),warn=True,encoding='utf8')
                c.run("""su -l %s -c "echo 'host all %s 0.0.0.0/0  md5' >> %s/master/seg-1/pg_hba.conf && source /home/%s/.bashrc &&  gpstop -u" """%(superuser,superuser,data_prefix,superuser),pty=True)
            c.clear()

    def pre_env(self):
        pin=self.pin
        common.hostname(pin)
        common.dns(pin)
        common.ssh(pin)

    def pre_cfg(self):
        pin=self.pin
        for conp in pin:
            with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
                cmd="""cat > /etc/sysctl.conf << EOF
                            kernel.shmall = 4000000000
                            kernel.shmmax = 500000000
                            kernel.shmmni = 4096
                            vm.overcommit_memory = 1
                            vm.overcommit_ratio = 95
                            net.ipv4.ip_local_port_range = 10000 65535 
                            kernel.sem = 500 2048000 200 40960
                            kernel.sysrq = 1
                            kernel.core_uses_pid = 1
                            kernel.msgmnb = 65536
                            kernel.msgmax = 65536
                            kernel.msgmni = 2048
                            net.ipv4.tcp_syncookies = 1
                            net.ipv4.conf.default.accept_source_route = 0
                            net.ipv4.tcp_max_syn_backlog = 4096
                            net.ipv4.conf.all.arp_filter = 1
                            net.core.netdev_max_backlog = 10000
                            net.core.rmem_max = 2097152
                            net.core.wmem_max = 2097152
                            vm.swappiness = 10
                            vm.zone_reclaim_mode = 0
                            vm.dirty_expire_centisecs = 500
                            vm.dirty_writeback_centisecs = 100
                            vm.dirty_background_ratio = 0 # See Note 5
                            vm.dirty_ratio = 0
                            vm.dirty_background_bytes = 1610612736
                            vm.dirty_bytes = 4294967296
                            EOF"""
                cmd=re.sub('\n\s*','\n',cmd)
                c.run(cmd,pty=True,encoding='utf8')
                c.run("sysctl -p",pty=True)
                cmd="""cat > /etc/security/limits.conf <<EOF
                        * soft nofile 524288
                        * hard nofile 524288
                        * soft nproc 131072
                        * hard nproc 131072
                        gpadmin soft nofile 524288
                        gpadmin hard nofile 524288
                        gpadmin soft nproc 131072
                        gpadmin hard nproc 131072
                        EOF
                      """
                cmd=cmd.replace('gpadmin',self.superuser)
                cmd=re.sub('\n\s*','\n',cmd)
                c.run(cmd,pty=True,encoding='utf8')

                cmd="chmod u+s /bin/ping"
                c.run(cmd,pty=True,encoding='utf8')

#gprpm_file="D:\\webroot\\common\\greenplum-6.5\\greenplum-db-6.5.0-rhel7-x86_64.rpm"
# m=gp(gprpm_file=gprpm_file)
# m.mirror=False
# m.standby_tag=True
# m.data()
# python_file="D:\\webroot\\common\\Python-3.7.4.tgz"
#java_file="D:\\webroot\\common\\jdk-8u151-linux-x64.rpm"

#m=gp(file=gprpm_file)
#m.total_new()
#m.total_new()
#m.java(java_file=java_file)
#m.pxf()
