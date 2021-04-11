##完全借助本地文件系统 3+2+10

from lmfinstall.greenplum.v2.core import gp 
import time 
from lmfinstall.ambari.v1.core import ambari 
from lmfinstall.greenplum.v2.ext import gp_ext 
from lmfinstall.fastdfs.v1.core import fdfs 
from lmf.tool import  mythread
from lmfinstall import common 
from lmfinstall.postgresql import postgresql1061
from lmfinstall.python import python 
import copy
from fabric import Connection
from lmf.dbv2 import db_command ,db_get_func_def,db_query,db_drop_func
from lmf.dbv2 import db_command_ext 
import re 
from lmf.tool import mythread
import os
import shutil 
from zljd.core.oss import oss 
import threading

#20200616京东云从零部署
class jd_web:
    def __init__(self,local_file_download=False):
        self.pin=[
                    ['root@10.0.64.32:22','BST@2020610','web1'],
                    ['root@10.0.64.33:22','BST@2020610','web2'],
                    ['root@10.0.64.34:22','BST@2020610','web3']
                    ]

        self.app5_1_pin=[
        ['root@10.0.64.35:22','BST@2020610','app1_db1'],

        ['root@10.0.64.36:22','BST@2020610','app5_db1master'],
        ['root@10.0.64.37:22','BST@2020610','app5_db1seg1'],
        ['root@10.0.64.38:22','BST@2020610','app5_db1seg2'],
        ['root@10.0.64.39:22','BST@2020610','app5_db1seg3'],
        ['root@10.0.64.40:22','BST@2020610','app5_db1seg4'],
        ]


        self.app5_2_pin=[
        ['root@10.0.64.41:22','BST@2020610','app1_db2'],

        ['root@10.0.64.42:22','BST@2020610','app5_db2master'],
        ['root@10.0.64.43:22','BST@2020610','app5_db2seg1'],
        ['root@10.0.64.44:22','BST@2020610','app5_db2seg2'],
        ['root@10.0.64.45:22','BST@2020610','app5_db2seg3'],
        ['root@10.0.64.46:22','BST@2020610','app5_db2seg4'],
        ]


        self.data_file_date=['20200629','20200624','20200629']
        self.web_file_date="20200629"


        self.oss_internal=True
        self.local_file_dir="D:\\jingdong_websys_download"
        self.local_file_download=local_file_download 
        self.gg_html=True
        self.init_host_cfg()
        self.init_local_file()
        self.init_oss_file()
        #

    def refresh_para(self):
        self.init_host_cfg()
        self.init_local_file()
        self.init_oss_file()

    def init_host_cfg(self):
        ip=self.app5_1_pin[0][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        self.db_host=ip

        ip=self.pin[2][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        self.redis_host=ip
        self.pg_master,self.pg_slave=self.app5_1_pin[0],self.app5_2_pin[0]

    def init_oss_file(self):
        self.pg_dmp_file_oss="/jdoss/backup/app1/app1_%s.dmp"%self.data_file_date[0]
        self.pg_dmp_file_gg_html_oss="/jdoss/backup/app1/app1_tb_public.gg_html_%s.dmp"%self.data_file_date[1]
        self.gp_dmp_file_oss="/jdoss/backup/app5/app5_db_biaost_%s.dmp"%self.data_file_date[2]

    def init_local_file(self):
        tmpdir=self.local_file_dir

        self.gp_file="%s\\greenplum-db-6.5.0-rhel7-x86_64.rpm"%tmpdir
        self.java_file="%s\\jdk-8u151-linux-x64.rpm"%tmpdir
        self.tomcat_file="%s\\apache-tomcat-8.5.56.tar.gz"%tmpdir
        self.redis_file="%s\\redis-4.0.2.tar.gz"%tmpdir
        self.pg_file="%s\\postgresql-10.6-1-linux-x64.run"%tmpdir
        self.python_file="%s\\Python-3.5.2.tgz"%tmpdir
        self.gpbackup_file="%s\\pivotal_greenplum_backup_restore-1.17.0-1-gp6-rhel-x86_64.gppkg"%tmpdir


        self.tomcat_web_file="%s\\fileroot.tar.gz"%tmpdir
        self.tomcat_image_file="%s\\images.tar.gz"%tmpdir
        self.tomcat_tar_file="%s\\tomcat.tar.gz"%tmpdir
        self.tomcat_apk_file="%s\\apk.tar.gz"%tmpdir

    def down_webfile(self):
        tmpdir=self.local_file_dir
        if self.local_file_download:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            files=['Python-3.5.2.tgz', 'apache-tomcat-8.5.56.tar.gz', 
            'greenplum-db-6.5.0-rhel7-x86_64.rpm', 'jdk-8u151-linux-x64.rpm', 'postgresql-10.6-1-linux-x64.run', 'redis-4.0.2.tar.gz'
            ,'pivotal_greenplum_backup_restore-1.17.0-1-gp6-rhel-x86_64.gppkg']
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
            files=['fileroot_%s.tar.gz'%self.web_file_date,'images_%s.tar.gz'%self.web_file_date,'tomcat_%s.tar.gz'%self.web_file_date,'apk_%s.tar.gz'%self.web_file_date]
            m=oss(conp='')
            m.internal=self.oss_internal
            for file in files:
                bg=time.time()
                filename='backup/web/'+file 
                print(file)
                file=file.replace('_'+self.web_file_date,'')
                m.down_file(filename,"%s/%s"%(tmpdir,file))
                ed=time.time()
                cost=int(ed-bg)
                print("totoal cost --%d s "%cost)

    def test(self):   
        for conp in self.pin:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            c.run("hostname && ip addr")

    def os_prt1(self):
        k='/dev/vdb'
        v='/data'
 
        for conp in self.pin[:2] :
            print(conp[2])

            common.mount(conp,k,v)

    #配置免密、hostname\dns
    def step_1(self):
        common.hostname(self.pin)
        common.dns(self.pin)
        common.ssh(self.pin)

    #jdk   
    def step_2(self):
        for conp in self.pin:
            common.java(conp,self.java_file)
        conp=self.pin[0]




    def step_3(self):
        for w in self.pin[:2]:
            self.step_3_(w,self.tomcat_file)

    #tomcat
    def step_3_(self,conp,sdir):

        tdir='/root/tom'
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        if  c.run("test -f %s/apache-tomcat-8.5.56.tar.gz"%tdir,pty=True,warn=True).failed:
        #     c.run("rm -rf %s/Python-3.5.2.tgz"%tdir,pty=True)
        # else:
            print("上传apache-tomcat-8.5.56.tar压缩包")
            c.put(sdir,tdir)
        c.run("mkdir -p /data/tomcat/tomcat")
        c.run("tar -zxvf %s/apache-tomcat-8.5.56.tar.gz -C /data/tomcat/tomcat"%tdir,pty=True)


    #tomcat 带数据版
    def step_4(self):
        for w in self.pin[:2]:
            self.step_4_(w,self.tomcat_tar_file)

    
    def step_4_(self,conp,sdir):

        tdir='/root/tom'
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        if  c.run("test -f %s/tomcat.tar.gz"%tdir,pty=True,warn=True).failed:
        #     c.run("rm -rf %s/Python-3.5.2.tgz"%tdir,pty=True)
        # else:
            print("上传tomcat.tar.gz压缩包")
            c.put(sdir,tdir)
        c.run("mkdir -p /data")
        c.run("tar -xvf %s/tomcat.tar.gz -C /"%tdir,pty=True)

    #redis
    def step_5(self):
        conp=self.pin[2]
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
        cmd="sed -i 's/^# requirepass foobared/requirepass redis/g' /etc/redis.conf "
        print(cmd)
        c.run(cmd)

        #启动
        cmd="cd /usr/local/bin && redis-server /etc/redis.conf"
        print(cmd)
        c.run(cmd)

        self.step_5_1()

    def step_5_1(self):
        for conp in self.pin[:2]:
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})

            ##securerandom.source=file:/dev/./urandom  ->  securerandom.source=file:/dev/./urandom
            cmd="sed -i 's/securerandom.source=file:\\/dev\\/random/securerandom.source=file:\\/dev\\/.\\/urandom/g' /usr/java/jdk1.8.0_151/jre/lib/security/java.security  "
            print(cmd)
            c.run(cmd)
        #nfs
    def step_6(self):
        conp1=self.pin[0]
        tdir="/data/cloud-upload"
        c1=Connection(conp1[0],connect_kwargs={"password":conp1[1]})
        if c1.run("test -f %s"%tdir,warn=True).failed:
            c1.run("mkdir -p %s"%tdir)

        c1.run("yum install -y nfs-utils && systemctl enable nfs-server && systemctl enable rpcbind  ",pty=True)
        ip=conp1[0]
        ip=ip[ip.index('@')+1:ip.index(':')]

        c1.run("echo '/data/cloud-upload  %s/24(rw,sync,no_root_squash)' > /etc/exports "%ip,pty=True)
        c1.run("exportfs -r ",pty=True)
        c1.run("systemctl start nfs-server",pty=True)

        conp2=self.pin[1]
        tdir="/data/cloud-upload"
        c2=Connection(conp2[0],connect_kwargs={"password":conp2[1]})
        if c2.run("test -f %s"%tdir,warn=True).failed:
            c2.run("mkdir -p %s"%tdir)
        c2.run("yum install  -y nfs-utils  && systemctl enable rpcbind ",pty=True)
        c2.run("systemctl start rpcbind ",pty=True)
        c2.run("showmount -e  %s "%ip,pty=True)
        c2.run("mount -t nfs %s:%s  %s "%(ip,tdir,tdir))

    #修改数据库\redis配置
    def step_7(self):
        db_host=self.db_host
        redis_host=self.redis_host
        for xm  in ['api','web']:
            dbfile="/data/tomcat/tomcat-api/webapps/lmbj-%s/WEB-INF/classes/resource/jdbc.properties"%xm
            redisfile="/data/tomcat/tomcat-api/webapps/lmbj-%s/WEB-INF/classes/resource/redis.properties"%xm

            conp1=self.pin[0]
            c=Connection(conp1[0],connect_kwargs={"password":conp1[1]})
            cmd="sed -i 's/[0-9]\\{2,3\\}\\.[0-9]\\{1,3\\}\\.[0-9]\\{1,3\\}\\.[0-9]\\{1,3\\}/%s/g'  %s "%(db_host,dbfile)
            print(cmd)
            c.run(cmd,pty=True )

            cmd="sed -i 's/[0-9]\\{2,3\\}\\.[0-9]\\{1,3\\}\\.[0-9]\\{1,3\\}\\.[0-9]\\{1,3\\}/%s/g'  %s "%(redis_host,redisfile)
            print(cmd)
            c.run(cmd,pty=True )


        ###
        # sql="""delete from  "public"."lmbj_user" where user_account not in ('18681507148','17198666491','13828744705')"""
        # db_command(sql,dbtype="postgresql",conp=['postgres','since2015',db_host,'biaost','public'])

    #nfs 图片解压
    def step_8(self):
        conp1=self.pin[0]
        c=Connection(conp1[0],connect_kwargs={"password":conp1[1]})
        tdir="/data"
        sdir=self.tomcat_web_file
        sdir1=self.tomcat_image_file
        sdir2=self.tomcat_apk_file
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)

        if  not c.run("test -f %s/fileroot.tar.gz"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/fileroot.tar.gz"%tdir,pty=True)
        print("fileroot.tar.gz压缩包")
        c.put(sdir,tdir)
        c.run("rm -rf /data/cloud-upload",pty=True)
        c.run("tar -xvf %s/fileroot.tar.gz -C /"%tdir,pty=True)

        if  not c.run("test -f %s/images.tar.gz"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/images.tar.gz"%tdir,pty=True)
        print("images.tar.gz压缩包")
        c.put(sdir1,tdir)
        c.run("rm -rf /data/images",pty=True)
        c.run("tar -xvf %s/images.tar.gz -C /"%tdir,pty=True)



        if  not c.run("test -f %s/apk.tar.gz"%tdir,pty=True,warn=True).failed:
            c.run("rm -rf %s/apk.tar.gz"%tdir,pty=True)
        print("apk.tar.gz压缩包")
        c.put(sdir2,tdir)
        c.run("rm -rf /data/apk",pty=True)
        c.run("tar -xvf %s/apk.tar.gz -C /"%tdir,pty=True)



    def web_start(self):

        conp1=self.pin[0]
        c=Connection(conp1[0],connect_kwargs={"password":conp1[1]})
        for xm in ['api','web']:
            cmd="/data/tomcat/tomcat-%s/bin/startup.sh"%(xm)
            print(cmd)
            c.run(cmd,pty=True)


    def web_prt(self):
        self.test()
        self.down_webfile()
        self.os_prt1()
        self.step_1()
        self.step_2()
        self.step_4()
        #redis
        self.step_5()
        #nfs
        self.step_6()

        #修改数据库\redis配置
        self.step_7()

        #图片文件
        self.step_8()

        self.web_start()







    def db_os_prt(self):
        for pin in [self.app5_1_pin,self.app5_2_pin]:
            common.hostname(pin)
            common.dns(pin)
            common.ssh(pin)

            k='/dev/vdb'
            v='/data'
            for conp in pin :
                print(conp[2])
                common.mount(conp,k,v)


    def db_app1_prt_restart(self):
        for conp in [self.app5_1_pin[0],self.app5_2_pin[0]]:
            k='/dev/vdb'
            v='/data'
            common.mount(conp,k,v)
        self.db_app1_prt()
        #self.db_app1_oss_pre()

    def db_app1_prt(self):
        #
        self.db_app1_oss_pre()
        #安装主从
        self.db_app1_prt1()

        #数据库依赖对象
        self.db_app1_prt2()

        #恢复除gg_html以外数据
        #1570
        self.db_app1_prt3()

        #恢复gg_html 数据（200G）
        if self.gg_html:
            self.db_app1_prt4()

        #PG函数替换
        self.db_app1_prt5()

        #PG服务器安装python包
        self.db_app1_prt6()

    def db_app1_prt1(self):
        #安装主从
        bg=time.time()
        conp1,conp2=self.pg_master,self.pg_slave
        postgresql1061.install(conp1,self.pg_file,pgdata="/data/postgresql",plpython="plpython35")
        try:
            python.install(conp1,self.python_file)
        except:
            print("python3.5安装小插曲")
        postgresql1061.install(conp2,self.pg_file,pgdata="/data/postgresql",plpython="plpython35")
        try:
            python.install(conp2,self.python_file)
        except:
            print("python3.5安装小插曲")
        postgresql1061.master_slave(conp1,conp2,"/data/postgresql","/data/postgresql")

        ed=time.time()

        cost=int(ed-bg)
        print("安装主从PG 共耗时 %d s"%cost)


    def db_app1_prt2(self):
        #创建角色
        ip=self.pg_master[0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        sql="create database biaost;"
        db_command_ext(sql,dbtype="postgresql",conp=['postgres','since2015',ip,'postgres','public'])


        extension=['plpython3u','pg_trgm','postgres_fdw','pgcrypto','dblink']
        for ext in extension:
            sql="create extension  %s"%ext
            print(sql)
            db_command(sql,dbtype="postgresql",conp=['postgres','since2015',ip,'biaost','public'])

        for user in ['app_reader','zl_reader']:
            sql1="create user app_reader with password 'app_reader';"
            sql2="grant usage on schema public to app_reader;"
            sql3="grant select on all tables in schema public to app_reader;"
            sql=sql1+sql2+sql3
            sql=sql.replace('app_reader',user)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=['postgres','since2015',ip,'biaost','public'])

        

    def db_app1_prt3(self):
        #恢复除开gg_html 以外的数据
        #上传数据 1540s
        conp=self.app5_1_pin[0]
        m_oss=oss(conp=conp)
        bg=time.time()
        ip=self.pg_master[0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        try:
            m_oss.mount()
            conp=self.app5_1_pin[0]

            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            cmd="export PGPASSWORD='since2015' &&  /opt/PostgreSQL/10/bin/pg_restore -c  -d biaost -U postgres -v  %s"%self.pg_dmp_file_oss
            print(cmd)
            c.run(cmd,warn=True)

            #sql="""delete from  "public"."lmbj_user" where user_account not in ('18681507148','17198666491')"""
            #db_command(sql,dbtype="postgresql",conp=['postgres','since2015',ip,'biaost','public'])

            

        except Exception as e:
            print(e)
        finally:
            m_oss.umount()
            print("umount")

        ed=time.time()
        cost=int(ed-bg)
        print("恢复app1.dmp(除开gg_html) 耗时 %d s "%cost)

    def db_app1_oss_pre(self):
        conp=self.app5_1_pin[0]
        m=oss(conp=conp)
        m.s3fs_pre()


    def db_app1_prt4(self):
        conp=self.app5_1_pin[0]
        m_oss=oss(conp=conp)
        bg=time.time()
        try:
            m_oss.mount()
            conp=self.app5_1_pin[0]

            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            cmd="export PGPASSWORD='since2015' &&  /opt/PostgreSQL/10/bin/pg_restore -d biaost -U postgres -v %s"%self.pg_dmp_file_gg_html_oss
            print(cmd)
            c.run(cmd,warn=True)


        except Exception as e:
            print(e)
        finally:
            m_oss.umount()
            print("umount")

        ed=time.time()
        cost=int(ed-bg)
        print("恢复gg_html 耗时 %d s "%cost)

    def db_app1_prt5(self):
        ip=self.pg_master[0]
        ip=ip[ip.index('@')+1:ip.index(':')]

        ip2=self.app5_1_pin[1][0]
        ip2=ip2[ip2.index('@')+1:ip2.index(':')]
        conp=['postgres','since2015',ip,'biaost','public']
        df=db_query("select 'public.'||proname as proname from pg_proc  where proname~'^get|^query|^count_' order by proname ",dbtype="postgresql",conp=conp)
        arr=df['proname'].tolist()
        #arr=["public.get_gg"]
        for name in arr:
            
            df=db_get_func_def(name,dbtype="postgresql",conp=conp)

            if df.empty:continue
            for i in df.index:
                func=df.iat[i,1]

                func=re.sub('hostaddr=[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3} port=[0-9]{1,5}','hostaddr=%s port=6432 dbname=biaost'%ip2,func)
                
                db_command(func,dbtype="postgresql",conp=conp)
                print(name,func[:100])
    
    def db_app1_prt6(self):

        conp1=self.app5_1_pin[0]
        c1=Connection(conp1[0],connect_kwargs={"password":conp1[1]})
        c1.run("/opt/python35/bin/python3 -m pip install pip==19.0.1  -i http://106.13.239.200/pypi --trusted-host=106.13.239.200",pty=True)
        c1.run("/opt/python35/bin/python3 -m pip install lmf==3.0.78 -i http://106.13.239.200/pypi --trusted-host=106.13.239.200",pty=True)

        conp2=self.app5_2_pin[0]
        c2=Connection(conp2[0],connect_kwargs={"password":conp2[1]})
        c2.run("/opt/python35/bin/python3 -m pip install pip==19.0.1  -i http://106.13.239.200/pypi --trusted-host=106.13.239.200",pty=True)
        c2.run("/opt/python35/bin/python3 -m pip install lmf==3.0.78 -i http://106.13.239.200/pypi --trusted-host=106.13.239.200",pty=True)

        pck=['pypinyin','python-Levenshtein']
        for p in pck:
            c1.run("/opt/python35/bin/python3 -m pip install %s  -i https://pypi.doubanio.com/simple"%p,pty=True)
            c2.run("/opt/python35/bin/python3 -m pip install %s  -i https://pypi.doubanio.com/simple"%p,pty=True)
    def db_app5_prt_restart(self):
        for pin in [self.app5_1_pin[1:],self.app5_2_pin[1:]]:
            common.hostname(pin)
            common.dns(pin)
            common.ssh(pin)

            k='/dev/vdb'
            v='/data'
            for conp in pin :
                print(conp[2])
                common.mount(conp,k,v)
        self.db_app5_prt()

    def db_app5_prt(self):
        self.db_app5_oss_pre()
        #安装软件
        self.db_app5_prt1()

        #用户和数据库准备
        self.db_app5_prt2()

        #hba
        self.db_app5_prt3()

        #app5.dmp
        #3870
        self.db_app5_prt4()

        #pgbouncer
        self.db_app5_prt5()

        #load balance
        self.db_app5_prt6()

        #pip
        self.db_app5_prt7()

    def db_app5_oss_pre(self):
        conp=self.app5_1_pin[1]
        m=oss(conp=conp)
        m.s3fs_pre()

        conp=self.app5_2_pin[1]
        m=oss(conp=conp)
        m.s3fs_pre()

    def db_app5_prt1(self):
        self.db_app5_prt1_tmp(self.app5_1_pin[1:])
        self.db_app5_prt1_tmp(self.app5_2_pin[1:])
    def db_app5_prt1_tmp(self,pin):
        bg=time.time()
        m=gp(file=self.gp_file,pin=pin)
        m.segs_pernode=3
        m.mirror=False
        m.pyver='3.5'
        m.data_prefix="/data/greenplum"
        m.standby_tag=False
        m.env_tag=False
        m.total_new(java_file=self.java_file,python_file=self.python_file)
        m.extension('pg_trgm')

        m1=gp_ext(pin=pin)
        m1.gpbackup_file=self.gpbackup_file
        m1.gpbackup()


        ed=time.time()
        cost=int(ed-bg)
        print("totally coast %d s"%cost)


    def db_app5_prt2(self):
        self.db_app5_prt2_tmp(self.app5_1_pin[1:])
        self.db_app5_prt2_tmp(self.app5_2_pin[1:])

    def db_app5_prt2_tmp(self,pin):
        bg=time.time()
        ip=pin[0][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        for user in ['app_reader','zl_reader','developer']:
            try:
                sql="""
                revoke all   on  ALL TABLES IN SCHEMA public   from  app_reader;  
                revoke all   on  database postgres  from  app_reader;  
                revoke all   on  schema public  from  app_reader  ;"""
                sql=sql.replace('app_reader',user)
                print(sql)
                db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])
                sql="drop user if exists %s  "%user 
                print(sql)
                db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])
            except Exception as  e:
                print(e)

        sql1="create user app_reader with password 'since2015';"
        sql2="grant usage on schema public to app_reader;"
        sql3="grant select on all tables in schema public to app_reader;"
        sql=sql1+sql2+sql3
        print(sql)
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])

        sql1="create user zl_reader with password 'zl_reader';"
        sql2="grant usage on schema public to zl_reader;"
        sql3="grant select on all tables in schema public to zl_reader;"
        sql=sql1+sql2+sql3
        print(sql)
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])

        sql="create user developer with superuser password 'zhulong!123';"
        print(sql)
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])

        sql="select pg_terminate_backend(pid) from pg_stat_activity where datname='biaost' "
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])
        sql="drop database if exists biaost;"
        db_command_ext(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])
        sql="create database  biaost;"
        db_command_ext(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'postgres','public'])

        sql="create extension  pg_trgm;"
        db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015',ip,'biaost','public'])

        #pg_trgm

        ed=time.time()
        cost=int(ed-bg)
        print("totally coast %d s"%cost)


    def db_app5_prt3(self):
        self.db_app5_prt3_tmp(self.app5_1_pin[1:])
        self.db_app5_prt3_tmp(self.app5_2_pin[1:])

    def db_app5_prt3_tmp(self,pin):
        conp=pin[0]
        ip=conp[0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        hba="""
        host  all  developer  10.0.64.58/24  md5
        host  all  app_reader 10.0.64.58/24 md5
        host  all  zl_reader  10.0.64.58/24  md5
        local  all  developer  ident
        """
        hba=hba.replace('10.0.64.58',ip)
        hba=re.sub('\n\s*','\n',hba)
        c.run("sed -i '/all\\s\\{1,5\\}developer/d' /data/greenplum/master/seg-1/pg_hba.conf ",pty=True)
        c.run("sed -i '/all\\s\\{1,5\\}app_reader/d' /data/greenplum/master/seg-1/pg_hba.conf ",pty=True)
        c.run("sed -i '/all\\s\\{1,5\\}zl_reader/d' /data/greenplum/master/seg-1/pg_hba.conf ",pty=True)
        c.run("echo '%s' >> /data/greenplum/master/seg-1/pg_hba.conf  "%hba,pty=True)
        c.run("su -l gpadmin -c 'gpstop -u'",pty=True)


    def db_app5_prt4(self):
        def f(num):
            if num==1:
                self.db_app5_prt4_tmp(self.app5_1_pin[1:])
            if num==2:
                self.db_app5_prt4_tmp(self.app5_2_pin[1:])
        mythread(f=f,arr=[1,2]).run(2)

    def db_app5_prt4_tmp(self,pin):
        #6300 s 
        conp=pin[0]
        m_oss=oss(conp=conp)
        bg=time.time()
        try:
            m_oss.mount()
            c=Connection(conp[0],connect_kwargs={"password":conp[1]})
            cmd="su -l gpadmin -c 'pg_restore -d biaost -U gpadmin -v   %s' "%self.gp_dmp_file_oss
            print(cmd)
            c.run(cmd,warn=True)


        except Exception as e:
            print(e)
        finally:
            m_oss.umount()
            print("umount")

        ed=time.time()
        cost=int(ed-bg)
        print("恢复app5.dmp 耗时 %d s "%cost)


    def db_app5_prt5(self):
        self.db_app5_prt5_tmp(self.app5_1_pin[1:])
        self.db_app5_prt5_tmp(self.app5_2_pin[1:])
        
    def db_app5_prt5_tmp(self,pin):
        conp=pin[0]
        ip=conp[0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        pgbouncer="""
         [databases]
         biaost = host=%s port=5432 dbname=biaost pool_size=200

         [pgbouncer]
         listen_port = 6432
         listen_addr = *
         auth_type = md5
         auth_file = /usr/local/greenplum-db/bin/userlist.txt
         logfile = pgbouncer.log
         pidfile = pgbouncer.pid
         admin_users = app_reader
         max_client_conn = 1000
         pool_mode = statement
        """%(ip)
        pgbouncer=re.sub('\n\s*','\n',pgbouncer)
        c.run("echo '%s' > /usr/local/greenplum-db/bin/pgbouncer.ini "%pgbouncer,pty=True)
        userlist=""""app_reader" "since2015" """
        c.run("echo '%s' >  /usr/local/greenplum-db/bin/userlist.txt  "%userlist,pty=True)

        c.run("su -l gpadmin -c 'cd /usr/local/greenplum-db/bin && ./pgbouncer -R -d pgbouncer.ini' ",pty=True)

    ##balance by nginx 
    def db_app5_prt6(self):
        conp=self.app5_1_pin[1]
        ip1=conp[0]
        ip1=ip1[ip1.index('@')+1:ip1.index(':')]

        conp2=self.app5_2_pin[1]
        ip2=conp2[0]
        ip2=ip2[ip2.index('@')+1:ip2.index(':')]
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        c.run("systemctl stop nginx",pty=True,warn=True)
        c.run("yum remove -y nginx",pty=True)
        c.run("yum install -y nginx",pty=True)

        cfg="""stream {
                    upstream app5 {
                        server %s:6432;
                        server %s:6432;
                    }
                    server {
                        listen 6433;
                        proxy_pass app5;
                    }
                }"""%(ip1,ip2)
        print(cfg)
        c.run("echo  '%s' >> /etc/nginx/nginx.conf "%cfg,pty=True)
        c.run("systemctl enable nginx",pty=True)
        c.run("systemctl start nginx",pty=True)

    #pip
    def db_app5_prt7(self):
        pck=['pip==19.0.1','python-Levenshtein','pypinyin']
        pin1=self.app5_1_pin[1:]
        pin2=self.app5_2_pin[1:]
        for pin in [pin1,pin2]:
            for conp in pin:
                c=Connection(conp[0],connect_kwargs={"password":conp[1]})
                for p in pck:
                    c.run("/opt/python35/bin/python3 -m pip install %s  -i https://jacky:Jacky666.@www.zhulong.com.cn/pypi/simple "%p,pty=True)



    def fdfs_part(self):
        pass 


    def fdfs_prt1(self):

        pass 

    def app_db(self):
        pass 
    def app1_db(self):
        pass 

    def pro1(self):
        self.web_prt()

        self.db_os_prt()
        t1=threading.Thread(target=self.db_app1_prt)
        t2=threading.Thread(target=self.db_app5_prt)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # def mf(num):
        #     if num==1:
        #         self.db_app1_prt()
        #     if num==2:
        #         self.db_app5_prt()
        # mythread(f=mf,arr=[1,2]).run(2)

        

        




        #启动tomcat
        ##self.step_8()




        #nfs

        #数据代码的恢复
        #启动服务

 

        pass




    # from lmfinstall.fastdfs.v1.core import fdfs 

    # pin=[
    #     ["root@192.168.4.206:22","rootBSTdb4@zhulong.com.cn","mdw","tracker:/data/fdfs/tracker:22122"] ,
    #     ["root@192.168.4.203:22","rootBSTdb1@zhulong.com.cn","sdw2","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000"] ,
    #     ["root@192.168.4.205:22","rootBSTdb2@zhulong.com.cn","standby","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  ,
    #     ["root@192.168.4.204:22","rootBSTdb3@zhulong.com.cn","sdw3","storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  ,
    #     ["root@192.168.4.202:22","rootBSTdb5@zhulong.com.cn","sdw1","storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  
    #     ]


    # m=fdfs(pin=pin)
    # m.from_zero()
##借助于 oss

# m=jd_web(False)

# m.db_app1_prt5()
# m.db_app1_prt6()
# m.db_app5_prt7()
# m=oss(conp=['root@10.0.64.51:22','BST@2020610','web1'])
# m.mount()

class jd_web_exam(jd_web):
    def __init__(self,local_file_download=False):
        super().__init__(local_file_download=local_file_download)
        self.pin= [
        ['root@10.0.64.47:22','BST@web2020610','web1'],
        ['root@10.0.64.48:22','BST@web2020610','web2'],
        ['root@10.0.64.49:22','BST@web2020610','web3']
                    ]

        self.app5_1_pin=[
        ['root@10.0.64.51:22','BST@web2020610','app1_db1'],

        ['root@10.0.64.52:22','BST@web2020610','app5_db1master'],
        ['root@10.0.64.53:22','BST@web2020610','app5_db1seg1'],
        ['root@10.0.64.54:22','BST@web2020610','app5_db1seg2'],
        ['root@10.0.64.55:22','BST@web2020610','app5_db1seg3'],
        ['root@10.0.64.56:22','BST@web2020610','app5_db1seg4'],
        ]


        self.app5_2_pin=[
        ['root@10.0.64.57:22','BST@web2020610','app1_db2'],

        ['root@10.0.64.58:22','BST@web2020610','app5_db2master'],
        ['root@10.0.64.59:22','BST@web2020610','app5_db2seg1'],
        ['root@10.0.64.60:22','BST@web2020610','app5_db2seg2'],
        ['root@10.0.64.61:22','BST@web2020610','app5_db2seg3'],
        ['root@10.0.64.11:22','BST@web2020610','app5_db2seg4'],
        ]
        self.data_file_date=['20200716','20200624min','20200629']
        self.web_file_date="20200716"
        self.local_file_dir="D:\\jingdong_websys_download1"
        self.refresh_para()

    def fdfs(self):
        pin_ext=["tracker:/data/fdfs/tracker:22122" ,
            "storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000",
            "storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000" ,
            "storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000" ,
            "storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"  
            ]
        pin=[]
        for w1,w2 in zip(self.app5_2_pin[1:],pin_ext):
            pin.append([*w1,w2])
        print(pin)
        m=fdfs(pin=pin)

        m.from_zero()

    def task(self):
        #29470
        bg=time.time()


        self.pro1()
        self.fdfs()

        ed=time.time()
        cost=int(ed-bg)
        #60000s
        print("totally--cost %d s"%cost)

def task1():
    ##29400
    from zljd.core.sdk import sdk  
    sdk().rebuild_hosts('web')
    sdk().rebuild_hosts('app5_1')
    sdk().rebuild_hosts('app5_2')
    m=jd_web_exam(True)
    m.gg_html=False
    m.task()

if __name__=='__main__':
    # m=jd_web_exam(False)
    # m.fdfs()
    task1()

  