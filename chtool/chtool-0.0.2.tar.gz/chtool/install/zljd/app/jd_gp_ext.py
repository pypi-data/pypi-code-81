from lmf.tool import mythread 
from fabric import Connection
from invoke import Responder
from lmfinstall.greenplum.v2.ext import gp_ext 
from zlgp3.dm2.c_function import gp_c_function
from lmf.dbv2 import db_command ,db_command_ext
import os 
from zljd.core.oss import oss 
from zljd.backup.restore import restore 
import shutil
import time ,sys
from zljd.app.jd_gp_data import jd_gp_data
# conp=['root@10.0.64.46:22','BST@2020610','datanode15']
# m_oss=oss(conp=conp)
# m_oss.mount()
class jd_gp_ext:
    def fs(f):
        ##nfs  oss 
        def wrap(*arg,**karg):
            if arg[0].fstype=='jdoss':
                conp=arg[1]
                m_oss=oss(conp=conp)
                bg=time.time()
                #name=re.
                try:
                    m_oss.mount()
                    f(*arg,**karg)
                except Exception as e:
                    print(e)
                finally:
                    m_oss.umount()
                    print("umount")
                ed=time.time()
                cost=int(ed-bg)
                print("  耗时 %d s "%(cost))
            elif arg[0].fstype=='nfs':
                print("nfs")
        return wrap
    
    def __init__(self):
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
        
        self.fstype="jdoss"

        
        self.gp_pin=self.pin[4:]
        ip=self.gp_pin[0][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        self.gp_master=['gpadmin','since2015',ip,'base_db','public']

        self.local_file_dir="D:\\jingdong_gpext_download"
        self.oss_internal=True
        self.docker_file="docker_ljt_20200605.tar"
        self.gpbackup_file="pivotal_greenplum_backup_restore-1.17.0-1-gp6-rhel-x86_64.gppkg"
        self.dmpdate='20200716'
        self.loc='jdyun'

        self.bstpasswd_file='C:\\Users\\Administrator\\.bstpasswd.ini'
        pass 

    #haolp.so+csv
    #plcontainer
    #redis
    #
    def env(self):

        self.gpbackup()
        #self.cgroup()
        self.plcontainer()
        self.ssh_run("yum install -y mysql-devel")
        self.ssh_run("yum install glib2-devel  glib  -y")

        self.pip_install("wheel")
        self.pip_install("mysqlclient")
        self.pip_install("zlgp3")
        self.pip_install("py3Fdfs")
        self.pip_install("zlgg")
        self.pip_install("zlparse==1.7.1128")
        self.pip_install('w3lib')
        self.pip_install('redis')
        self.pip_install('zlpage')
        self.pip_install('pillow')
        self.redis()
        self.db_env1()
        self.add_data(loc=self.loc)
        gp_c_function(loc=self.loc).add_so()
        gp_c_function(loc=self.loc).flush_csv()

        self.db_env2()
        pass

    def redis(self):
        tmpdir=self.local_file_dir
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)
        files=['redis-4.0.2.tar.gz']
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

        self.redis_file="%s\\redis-4.0.2.tar.gz"%tmpdir

        conp=self.gp_pin[1]
        tdir='/root/redis'
        sdir=self.redis_file
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        if  not c.run("test -f %s/redis-4.0.2.tar.gz"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/redis-4.0.2.tar.gz"%tdir,pty=True)
        else:
            print("上传redis-4.0.2.tar.gz压缩包")
            c.put(sdir,tdir)
        c.run("tar -zxvf %s/redis-4.0.2.tar.gz -C /root"%tdir,pty=True)

        ###编译安装
        c.run("cd /root/redis-4.0.2  && make MALLOC=libc   && make install ",pty=True)

        ###配文件
        c.run("cd /root/redis-4.0.2  && cp redis.conf /etc/redis.conf  ",pty=True)

        #修改bind 127.0.0.1 -->  bind  本机ip 127.0.0.1
        ip=conp[0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        cmd="sed -i 's/bind 127\\.0\\.0\\.1/bind %s 127\\.0\\.0\\.1/g' /etc/redis.conf "%ip
        print(cmd)
        c.run(cmd)

        ##daemonize no   -->daemonize yes
        cmd="sed -i 's/daemonize no/daemonize yes/g' /etc/redis.conf "
        print(cmd)
        c.run(cmd)

        ## requirepass foobared   requirepass redis
        cmd="sed -i 's/^# requirepass foobared/requirepass since2015/g' /etc/redis.conf "
        print(cmd)
        c.run(cmd)

        #启动
        cmd="cd /usr/local/bin && redis-server /etc/redis.conf"
        print(cmd)
        c.run(cmd)
    def plcontainer(self):
        tmpdir=self.local_file_dir

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
        files=[self.docker_file]
        m=oss(conp='')
        m.internal=self.oss_internal
        for file in files:
            bg=time.time()
            filename='backup/ext/'+file 
            print(file)
            m.down_file(filename,"%s/%s"%(tmpdir,file))
            ed=time.time()
            cost=int(ed-bg)
            print("totoal cost --%d s "%cost)


        m=gp_ext(pin=self.gp_pin)
        m.docker_file="%s\\%s"%(tmpdir,self.docker_file)
        m.plcontainer()
        m.plcontainer_prt1()
        #self.fs_pre()
        #self.plcontainer_prt_oss(self.docker_file)

    def plcontainer_prt_oss(self,filename):
        conp=self.gp_pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
            c.run("su -l gpadmin -c 'plcontainer image-delete -i swf:ljt' ",pty=True,warn=True)
        def f1(conp):
            self.plcontainer_prt_oss_f(conp,filename)
        mythread(f=f1,arr=self.gp_pin).run(num=len(self.gp_pin))

        conp=self.gp_pin[0]
        with Connection(conp[0],connect_kwargs={"password":conp[1]}) as c:
            asw1=Responder("Yy|Nn","Y\n")
            c.run("su -l gpadmin -c 'gpstop -M immediate' ",pty=True,watchers=[asw1])
            c.run("su -l gpadmin -c 'gpstart -a -B 15' ",pty=True)

    @fs
    def plcontainer_prt_oss_f(self,conp,filename):
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        c.run("su -l gpadmin -c 'docker load -i /jdoss/backup/ext/%s' "%filename)

    def cgroup(self):
        m=gp_ext(pin=self.gp_pin)
        m.cgroup()

    def gpbackup(self):
        tmpdir=self.local_file_dir

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
        files=[self.gpbackup_file,'gpbackup','gprestore']
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


        m=gp_ext(pin=self.gp_pin)
        m.gpbackup_file="%s\\%s"%(tmpdir,self.gpbackup_file)
        m.gpbackup()

        print("gpbackup gprestore 更换")

        conp=self.gp_pin[0]
        tdir='/root/gpbackup-ext'
        sdir="%s\\gpbackup"%(tmpdir)
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        if  not c.run("test -f %s/gpbackup"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/gpbackup"%tdir,pty=True)

        print("上传gpbackup压缩包")
        c.put(sdir,tdir)

        sdir="%s\\gprestore"%(tmpdir)
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        if  not c.run("test -f %s/gprestore"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/gprestore"%tdir,pty=True)
        print("gprestore")
        c.put(sdir,tdir)

        c.run("cp /root/gpbackup-ext/gpbackup  /usr/local/greenplum-db/bin/gpbackup",pty=True)
        c.run("cp /root/gpbackup-ext/gprestore  /usr/local/greenplum-db/bin/gprestore",pty=True)
        c.run("""for i in {1..15};do scp /root/gpbackup-ext/gprestore /root/gpbackup-ext/gpbackup  root@datanode$i:/usr/local/greenplum-db/bin ;done  """,pty=True)
        c.run("""scp /root/gpbackup-ext/gprestore /root/gpbackup-ext/gpbackup  root@master4:/usr/local/greenplum-db/bin  """,pty=True)

    def fs_pre(self):
        if self.fstype=="jdoss":
            def f1(conp):
                m_oss=oss(conp=conp)
                m_oss.s3fs_pre()
            mythread(f=f1,arr=self.gp_pin[1:]).run(len(self.gp_pin[1:]))

    def pip_install(self,pkg):
        self.ssh_run("/opt/python35/bin/python3 -m pip install %s --no-cache-dir -i http://lanmengfei:since2015@www.biaoshitong.com/bstdata/pypi/simple --trusted-host www.biaoshitong.com "%pkg,num=17)

    def ssh_run(self,cmd,num=10):
        if num==1:
            for conp in self.gp_pin:
                c=Connection(conp[0],connect_kwargs={"password":conp[1]})
                c.run("hostname")
                c.run(cmd,pty=True)
        else:
            def f(conp):
                c=Connection(conp[0],connect_kwargs={"password":conp[1]})
                c.run("hostname")
                c.run(cmd,pty=True)
            mythread(f=f,arr=self.gp_pin).run(num=num)


    def db_env1(self):
        #hba
        conp=self.gp_pin[0]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        hba_path=os.path.join(os.path.dirname(__file__) ,'pg_hba.conf' ) if __name__!='__main__' else os.path.join( os.path.dirname(sys.argv[0]) ,'pg_hba.conf')
        with open(hba_path,'r',encoding='utf8') as f :
            content=f.read()
        c.run("echo  '%s' >> /data/greenplum/master/seg-1/pg_hba.conf"%content)
        c.run("su -l gpadmin -c 'gpstop -u' ",pty=True)
        #c.run("echo  'host all all 0.0.0.0/0  md5' >> /data/greenplum/master/seg-1/pg_hba.conf")
        
        #bstpasswd 
        c.put(self.bstpasswd_file,'/root')
        c.run("""for i in {1..15};do scp /root/.bstpasswd.ini   root@datanode$i:/root ;done  """,pty=True)
        c.run("""scp /root/.bstpasswd.ini  root@master4:/root   """,pty=True)


        c.run("su -l gpadmin -c 'gpconfig -c shared_buffers -v 1250MB' ",pty=True)
        #statement_mem=1250MB
        c.run("su -l gpadmin -c 'gpconfig -c statement_mem -v 1250MB' ",pty=True)
        asw1=Responder("Yy|Nn","Y\n")
        c.run("su -l gpadmin -c 'gpstop -M immediate' ",pty=True,watchers=[asw1])
        c.run("su -l gpadmin -c 'gpstart -a -B 15' ",pty=True)
        c.run("su -l gpadmin -c 'plcontainer runtime-add -r ljt -i swf:ljt -l python3' ",pty=True)

    def db_env2(self):
        sqls=["create extension if not exists plcontainer;","create schema if not exists cdc"]
        for sql in sqls:
            print(sql)
            db_command(sql,dbtype="postgresql",conp=self.gp_master)


        sql="create resource queue developer with (active_statements=40,memory_limit='6192MB')"
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.gp_master)
        print(sql)
        sql="alter user developer with resource queue developer"
        db_command_ext(sql,dbtype="postgresql",conp=self.gp_master)
        conp=self.gp_pin[0]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        asw1=Responder("Yy|Nn","Y\n")
        c.run("su -l gpadmin -c 'gpstop -M immediate' ",pty=True,watchers=[asw1])
        c.run("su -l gpadmin -c 'gpstart -a -B 15' ",pty=True)


    def add_data(self,loc):
        m=jd_gp_data()
        #schem_src 9300/10000
        m.add_data1(loc=loc,dmpdate=self.dmpdate)

def task1():
    m=jd_gp_ext()
    m.env()


def task2():
    from zlgp3.dm2.usage import usage 
    usage(loc='jdyun').from_zero()

if __name__=='__main__':
    #task1()
    loc='jdyun'
    dmpdate='20200823'
    m=jd_gp_ext()
    m.pip_install('mysqlclient')

    # conp=m.gp_pin[0]
    # c=Connection(conp[0],connect_kwargs={"password":conp[1]})
    # c.put(m.bstpasswd_file,'/root')
    # c.run("""for i in {1..15};do scp /root/.bstpasswd.ini   root@datanode$i:/root ;done  """,pty=True)
    # c.run("""scp /root/.bstpasswd.ini  root@master4:/root   """,pty=True)

    # gp_c_function(loc=m.loc).add_so()
    # gp_c_function(loc=m.loc).flush_csv()

    # m.db_env2()


    pass

"""
host all gpadmin 0.0.0.0/0  md5
host all all 10.0.64.52/32  md5
host all all 10.0.64.53/32  md5
host all all 10.0.64.54/32  md5
host all all 10.0.64.55/32  md5
host all all 10.0.64.56/32  md5
host all all 10.0.64.25/32  md5
host all all 10.0.64.51/32  md5

host all all 10.0.64.57/32  md5
host all all 10.0.64.58/32  md5
host all all 10.0.64.59/32  md5
host all all 10.0.64.60/32  md5
host all all 10.0.64.61/32  md5
host all all 10.0.64.11/32  md5


#self
host  all  all  10.0.64.30/32 md5

# lch
host all all 10.0.64.20/32 md5

#blj
host all all 10.0.64.3/32 md5

#host all all 10.0.64.12/32 md5 
#host all all 10.0.64.13/32 md5
#host all all 10.0.64.14/32 md5
#host all all 10.0.64.15/32 md5
#host all all 10.0.64.16/32 md5
#host all all 10.0.64.17/32 md5
#host all all 10.0.64.18/32 md5
#host all all 10.0.64.19/32 md5
"""


"""
/opt/python35/bin/python3 -m pip install  mysqlclient
"""