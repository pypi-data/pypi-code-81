
import time 
from lmf.tool import  mythread
from lmfinstall import common 
import copy
from fabric import Connection
from lmf.dbv2 import db_command_ext ,db_command,db_query
import shutil 
from zljd.core.oss import oss 
from zljd.settings import gp_settings
import os

#负责恢复oss里的dmp 文件到应用数据库中
#挂载的文件系统、app应用、PG 和GP 、命名规则
#gp_tb_dm.t_zz_20200629.dmp




#19872403

class restore_base:
    def fs(f):
        ##nfs  oss 
        def wrap(*arg,**karg):
            if arg[0].fstype=='jdoss':
                conp=arg[0].conp_ssh
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
    
    def __init__(self,loc='jdyun',app='gp'):
        self.fstype="jdoss"
        self.conp_ssh=["root@10.0.64.21:22","BST@2020610"]
        self.conp=['postgres','since2015','10.0.64.21','base_db','public']
        #恢复的目标数据库蕴含在conp里
        self.pg_dump_dir="/opt/PostgreSQL/10/bin/pg_restore"
        self.app,self.loc=app,loc
        self.fsdir="/jdoss/backup/%s"%app
        if self.app in ['app1','db1','db2','db3','db4']:
            self.app_type='pg'
        else:
            self.app_type='gp'
        self.m_oss=oss(conp=self.conp_ssh)
        if not self.loc.startswith('jdyun'):self.m_oss.internal=False

    def fs_pre(self):
        if self.fstype=="jdoss":
            m_oss=oss(conp=self.conp_ssh)
            m_oss.s3fs_pre()


        

    @fs
    def tb_gp(self,tablename,dmpdate):
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        sql="drop table if exists %s "%tablename 
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        dmpdates=dmpdate.split(",")
        for dmpdate in dmpdates:
            user,password,host,db,schema=self.conp
            file=self.fsdir+"/"+"%s_tb_%s_%s.dmp"%(self.app,tablename,dmpdate)
            file_key=file[len(self.m_oss.mount_dir)+1:]
            print(file_key)
            if len(self.m_oss.list_dir(file_key[:-2]))==0:continue
            c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
            cmd="""su -l gpadmin -c "pg_restore -d %s -v %s" """%(db,file)
            print(cmd)
            c.run(cmd,pty=True,warn=True)



    @fs
    def tb_pg(self,tablename,dmpdate):
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        sql="drop table if exists %s "%tablename 
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        dmpdates=dmpdate.split(",")
        for dmpdate in dmpdates:
            user,password,host,db,schema=self.conp

            file=self.fsdir+"/"+"%s_tb_%s_%s.dmp"%(self.app,tablename,dmpdate)
            file_key=file[len(self.m_oss.mount_dir)+1:]
            print(file_key)
            if len(self.m_oss.list_dir(file_key[:-2]))==0:continue
            c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
            cmd="""export PGPASSWORD='%s' &&  %s -U postgres -d %s -v %s """%(password,self.pg_dump_dir,db,file)
            print(cmd)
            c.run(cmd,pty=True,warn=True)

    def tb(self,tablename,dmpdate):
        if self.app_type=='pg':
            self.tb_pg(tablename,dmpdate)
        elif self.app_type=='gp':
            self.tb_gp(tablename,dmpdate)

    def tb1(self,tablename,dmpdate,leaf=False):
        dmpdate=self.get_oss_dmpdate('tb',tablename,dmpdate)
        name=tablename
        sp=gp_settings[self.loc]['conp_%s_superuser'%self.app]
        folder_name="backup/%s/tb_%s"%(self.app,name)
        cfg=self.m_oss.get_gpbackup_yaml(folder_name)

        bg=time.time()
        conp=self.conp_ssh
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        cmd="""su -l %s -c "echo '%s' >/home/%s/s3-%s-config.yaml " """%(sp,cfg,sp,self.app)
        #print(cmd)
        c.run(cmd)
        user,password,ip,db,schema=self.conp
        sql="drop table if exists %s "%tablename
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        if not leaf:
            cmd="""su -l %s -c "gprestore  --include-table %s --timestamp %s --plugin-config /home/%s/s3-%s-config.yaml" """%(sp,name,dmpdate,sp,self.app)
        else:
            cmd="""su -l %s -c "gprestore  --include-table %s --leaf-partition-data  --on-error-continue  --timestamp %s --plugin-config /home/%s/s3-%s-config.yaml" """%(sp,name,dmpdate,sp,self.app)
        #print(cmd)
        c.run(cmd)

        cmd="""su -l %s -c "rm -rf /home/%s/s3-%s-config.yaml " """%(sp,sp,self.app)
        c.run(cmd)

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)




    @fs
    def schema_gp(self,schemaname,dmpdate):
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        sql="drop schema if exists %s cascade "%schemaname 
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        user,password,host,db,schema=self.conp
        file=self.fsdir+"/"+"%s_schema_%s_%s.dmp"%(self.app,schemaname,dmpdate)
        c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
        cmd="""su -l gpadmin -c "pg_restore -d %s -v %s" """%(db,file)
        print(cmd)
        c.run(cmd,pty=True,warn=True)


    @fs
    def schema_pg(self,schemaname,dmpdate):
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        sql="drop schema if exists %s cascade "%schemaname 
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        user,password,host,db,schema=self.conp
        file=self.fsdir+"/"+"%s_schema_%s_%s.dmp"%(self.app,schemaname,dmpdate)
        c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
        cmd="""export PGPASSWORD='%s' &&  %s -U postgres -d %s -v %s """%(password,self.pg_dump_dir,db,file)
        print(cmd)
        c.run(cmd,pty=True,warn=True)

    def schema(self,schemaname,dmpdate):
        if self.app_type=='pg':
            self.schema_pg(schemaname,dmpdate)
        elif self.app_type=='gp':
            self.schema_gp(schemaname,dmpdate)


    def schema1(self,schemaname,dmpdate,leaf=False):
        dmpdate=self.get_oss_dmpdate('schema',schemaname,dmpdate)
        name=schemaname
        sp=gp_settings[self.loc]['conp_%s_superuser'%self.app]
        folder_name="backup/%s/schema_%s"%(self.app,name)
        cfg=self.m_oss.get_gpbackup_yaml(folder_name)

        bg=time.time()
        conp=self.conp_ssh
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        cmd="""su -l %s -c "echo '%s' >/home/%s/s3-%s-config.yaml " """%(sp,cfg,sp,self.app)
        #print(cmd)
        c.run(cmd)
        user,password,ip,db,schema=self.conp
        sql="drop schema if exists %s cascade  "%schemaname
        print(sql)
        db_command(sql,dbtype="postgresql",conp=self.conp)
        if not leaf:
            cmd="""su -l %s -c "gprestore  --include-schema %s --timestamp %s --plugin-config /home/%s/s3-%s-config.yaml" """%(sp,name,dmpdate,sp,self.app)
        else:
            cmd="""su -l %s -c "gprestore  --include-schema %s --leaf-partition-data  --on-error-continue  --timestamp %s --plugin-config /home/%s/s3-%s-config.yaml" """%(sp,name,dmpdate,sp,self.app)
        #print(cmd)
        c.run(cmd)

        cmd="""su -l %s -c "rm -rf /home/%s/s3-%s-config.yaml " """%(sp,sp,self.app)
        c.run(cmd)

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)

    @fs
    def db_pg(self,dbname,dmpdate):
        if dbname=='postgres':
            self.conp[3]='template1'
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        sql="select pg_terminate_backend(pid) from pg_stat_activity where datname='%s'"%dbname
        db_command(sql,dbtype="postgresql",conp=self.conp)
        sql="drop database if exists %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)

        sql="create database  %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)

        user,password,host,db,schema=self.conp
        file=self.fsdir+"/"+"%s_db_%s_%s.dmp"%(self.app,dbname,dmpdate)
        c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
        cmd="""export PGPASSWORD='%s' &&  %s -U postgres -d %s -v %s """%(password,self.pg_dump_dir,dbname,file)
        print(cmd)
        c.run(cmd,pty=True,warn=True)

    @fs
    def db_gp(self,dbname,dmpdate):
        conp_ssh=self.conp_ssh
        ##"gp:base_db:tb:qyzz"
        if dbname=='postgres':
            self.conp[3]='template1'
        sql="select pg_terminate_backend(pid) from pg_stat_activity where datname='%s'"%dbname
        db_command(sql,dbtype="postgresql",conp=self.conp)
        sql="drop database if exists %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)

        sql="create database  %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)

        user,password,host,db,schema=self.conp
        file=self.fsdir+"/"+"%s_db_%s_%s.dmp"%(self.app,dbname,dmpdate)
        c=Connection(conp_ssh[0],connect_kwargs={"password":conp_ssh[1]})
        cmd="""su -l gpadmin -c "pg_restore -d %s -v %s" """%(dbname,file)
        print(cmd)
        c.run(cmd,pty=True,warn=True)

    def db(self,dbname,dmpdate):
        if self.app_type=='pg':
            self.db_pg(dbname,dmpdate)
        elif self.app_type=='gp':
            self.db_gp(dbname,dmpdate)
    def get_oss_dmpdate(self,obtype,name,dmpdate):
        folder_name="backup/%s/%s_%s/backups/%s/%s"%(self.app,obtype,name,dmpdate[:8],dmpdate)
        
        arr=self.m_oss.list_dir(folder_name)
        arr=sorted(list(arr))
        dt=arr[-1]
        dt=dmpdate+dt
        print(folder_name,dt)
        return dt 
    def db1(self,dbname,dmpdate):
        dmpdate=self.get_oss_dmpdate('db',schemaname,dmpdate)
        name=dbname
        sp=gp_settings[self.loc]['conp_%s_superuser'%self.app]
        folder_name="backup/%s/db_%s"%(self.app,name)
        cfg=self.m_oss.get_gpbackup_yaml(folder_name)

        bg=time.time()
        conp=self.conp_ssh
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        cmd="""su -l %s -c "echo '%s' >/home/%s/s3-%s-config.yaml " """%(sp,cfg,sp,self.app)
        print(cmd)
        c.run(cmd)
        user,password,ip,db,schema=self.conp

        if dbname=='postgres':
            print("GP里--postgres 数据库不支持drop ")
            return 
            self.conp[3]='postgres'
        sql="select pg_terminate_backend(pid) from pg_stat_activity where datname in('%s','template1')"%dbname
        db_command(sql,dbtype="postgresql",conp=self.conp)
        sql="drop database if exists %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)

        sql="create database  %s  "%dbname 
        print(sql)
        db_command_ext(sql,dbtype="postgresql",conp=self.conp)


        cmd="""su -l %s -c "gprestore    --timestamp %s --plugin-config /home/%s/s3-%s-config.yaml" """%(sp,dmpdate,sp,self.app)
        print(cmd)
        c.run(cmd)

        cmd="""su -l %s -c "rm -rf /home/%s/s3-%s-config.yaml " """%(sp,sp,self.app)
        c.run(cmd)

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost  %d s"%cost)

class restore(restore_base):
    def __init__(self,loc='jdyun',app='gp'):
        super().__init__(loc=loc,app=app)
        self.loc=loc
        self.app=app
        self.conp=copy.deepcopy(gp_settings[loc]['conp_%s'%app])
        self.conp_ssh=copy.deepcopy(gp_settings[loc]['conp_%s_ssh'%app])
        self.superuser=copy.deepcopy(gp_settings[loc]['conp_%s_superuser'%app])


        self.fsdir="/jdoss/backup"+"/"+app
 




def pro1():
    m=restore(loc='jdyun',app='gp')
    #['dm.zlqy_t_qy_zhuce']
    tb1=['dm.t_person_pre',"dm.t_file_upload"
        ,'dm.feiyan','dm.dst_gg_meta','dm.algo_m_gg']
    tb2=['dm.t_person','dm.t_zz']
    # for tb in tb1:
    #     m.tb1(tb,'20200823',leaf=True)
    for tb in tb2:
        m.tb(tb,'20200823')

if __name__=='__main__':
    # m=restore(loc='jdyun',app='gp')
    # m.tb1('dm.zlqy_t_qy_zhuce','20200822',leaf=True)
    #pro1()
    pass