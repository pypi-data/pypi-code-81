from fabric import Connection
from lmf.dbv2 import db_command_ext, db_command
from invoke import Responder
import psycopg2
from lmf.tool import mythread 
import os
import re
import time
import shutil 
from zljd.core.oss import oss 
## pin 中 主机排列规则
## 第一台为 airflow master
## 后面 为 airflow worker


# cmd中 "chcp 65001 就是换成UTF-8代码页"

class jd_airflow():

    def __init__(self,local_file_download=True):

        self.pin = [
            ["root@10.0.64.4:22", "BST@2020", "airflow_master"],
           
        ]
        self.airflow_cluster_pin=self.pin
        self.airflow_db_pin = ["root@10.0.64.4:22", "BST@2020", "airflow_db"]  ## airflow元数据库pin
        self.airflow_db = self.airflow_db_pin
        self.airflow_db_conp = ['postgres', 'since2015', re.findall('@(.+?):', self.airflow_db_pin[0])[0], 'postgres',
                                'public']
        self.airflow_setting = {'worker_concurrency': 18, 'workers': 8, 'parallelism': 180, 'max_threads': 50}

        self.oss_internal=True
        self.local_file_dir="D:\\jingdong_airflowsys_download"
        self.local_file_download=local_file_download 

        self.init_local_file()



    def init_local_file(self):
        tmpdir=self.local_file_dir

        self.redis_sdir = '%s\\redis-4.0.2.tar.gz'%tmpdir
        self.python_sdir = '%s\\Python-3.5.2.tgz'%tmpdir
        self.airmg_sdir = '%s\\airmg.sh'%tmpdir
        self.airflow_db_sdir = '%s\\postgresql-10.6-1-linux-x64.run'%tmpdir
        self.chrome_rpm='%s\\google-chrome-stable_current_x86_64.rpm'%tmpdir
        self.chrome_driver='%s\\chromedriver'%tmpdir
        self.dags='%s\\dags.tar.gz'%tmpdir


    def down_webfile(self):
        tmpdir=self.local_file_dir
        if self.local_file_download:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            files=['Python-3.5.2.tgz', 'airmg.sh', 
            'google-chrome-stable_current_x86_64.rpm', 'chromedriver', 'postgresql-10.6-1-linux-x64.run', 'redis-4.0.2.tar.gz','dags.tar.gz']
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



    def install(self):
        # self.down_webfile()
        # self.init_common()  # 配置免密,dns
        # self.install_python()  # 安装python
        self.install_pg()  # 安装 airflow 元数据库
        # self.create_database()  # 在元数据库中 创建 airflow 数据库
   
        # self.install_airflows()  # 安装 airflow
        # self.init_airflows()  # 初始化 airflow 集群
    

    def install_python(self):
        from lmfinstall.v2.python352 import install
        def f(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run('yum install -y patch')
            install(conp, self.python_sdir)

        mythread(f=f,arr=self.pin).run(len(self.pin))

    def init_common(self):
        from lmfinstall.common import hostname, dns, ssh
        hostname(self.airflow_cluster_pin)
        dns(self.airflow_cluster_pin)
        ssh(self.airflow_cluster_pin)

    def install_airflows(self):
        mythread(f=self.install_airflow,arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
        # for conp in self.airflow_cluster_pin:
        #     self.install_airflow(conp)

    def install_airflow(self, conp):

        c = Connection(conp[0], connect_kwargs={"password": conp[1]})
        c.run("/opt/python35/bin/python3 --version")
        c.run(
            "export SLUGIFY_USES_TEXT_UNIDECODE=yes && /opt/python35/bin/python3 -m pip install apache-airflow==1.10.3 psycopg2-binary  redis celery -i https://pypi.douban.com/simple",
            pty=True, encoding='utf8')
        c.run("""/opt/python35/bin/python3 -m pip install flask==1.0.4 -i https://pypi.douban.com/simple """)
        std = c.run('cat /etc/profile|grep AIRFLOW_HOME|wc -l', pty=True, hide=True).stdout

        if int(std) > 0:
            c.run('source /etc/profile && /opt/python35/bin/airflow', pty=True, warn=True)
        else:
            c.run(
                """echo  "export AIRFLOW_HOME=/opt/airflow"  >> /etc/profile  && source /etc/profile && /opt/python35/bin/airflow """,
                pty=True, warn=True)

        result = c.run('firewall-cmd --state', pty=True, warn=True, hide=True, encoding='utf8')
        if 'not running' not in result.stdout:
            c.run('firewall-cmd --permanent --zone=public --add-port=8793/tcp')
            c.run('firewall-cmd --reload')

        c.run('chmod 777 -R /opt/airflow')
   

    def install_pg(self):

        from lmfinstall.postgresql.postgresql1061 import install, plpython

        conp = self.airflow_db

        pgdata = '/data/postgresql/data'
        install(conp, self.airflow_db_sdir, plpython="plpython35",pgdata=pgdata)
        c = Connection(conp[0], connect_kwargs={"password": conp[1]})
        
        c.run("""sed -i 's/^max_connections = [0-9]*/max_connections = 500/g' %s/postgresql.conf""" % pgdata, pty=True)
        c.run("""systemctl restart postgresql-10.service""", pty=True)

    

    def restore_database(self):
        pass




    def create_database(self):
        conp = self.airflow_db_conp
        db_name = 'airflow'
        
        con = psycopg2.connect(database=conp[3], user=conp[0], password=conp[1], host=conp[2])
        con.autocommit = True
        cur = con.cursor()
        cur.execute('CREATE DATABASE {};'.format(db_name))
        cur.close()
        con.close()

    def init_airflows(self):
        mythread(f=self.init_airflow1,arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
        mythread(f=self.init_airflow2,arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
        # mythread(f=self.init_airflow3,arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
  
    def init_airflow1(self, conp):
        pg_passwd = self.airflow_db_conp[1]
        pg_host = self.airflow_db_conp[2]
        c = Connection(conp[0], connect_kwargs={"password": conp[1]})
        c.run('chmod 777 -R /opt/airflow')
        

        c.run('mkdir -p /opt/airflow/dags')
        c.run(
            """sed -i 's/^result_backend = db.*airflow$/result_backend = db+postgresql:\/\/postgres:{pg_passwd}@{pg_host}\/airflow/g' /opt/airflow/airflow.cfg """.format(
                pg_passwd=pg_passwd, pg_host=pg_host))
        
        c.run(
            """sed -i 's/^sql_alchemy_conn = sqlite.*airflow.db$/sql_alchemy_conn=postgresql:\/\/postgres:{pg_passwd}@{pg_host}\/airflow/g' /opt/airflow/airflow.cfg """.format(
                pg_passwd=pg_passwd, pg_host=pg_host))
        c.run("""sed -i 's/^default_timezone = utc/default_timezone = Asia\/Shanghai/g' /opt/airflow/airflow.cfg """)
        
        c.run("""sed -i 's/^catchup_by_default = True/catchup_by_default = False/g' /opt/airflow/airflow.cfg """)
        c.run('source /etc/profile && /opt/python35/bin/airflow initdb')
    def init_airflow2(self, conp):
       
        c = Connection(conp[0], connect_kwargs={"password": conp[1]})

        otweb = c.run(""" ps -ef |grep webserver|grep -v grep|grep -v bash|awk '{print $2}' | wc -l """,
                      hide=True).stdout

        if int(otweb) > 0:
            c.run("""ps -ef |grep webserver|grep -v grep|grep -v bash|awk '{print $2}'|xargs kill -9 """)

        otsch = c.run("""ps -ef |grep scheduler|grep -v grep|grep -v bash|awk '{print $2}' | wc -l """,
                      hide=True).stdout

        if int(otsch) > 0:
            c.run("""ps -ef |grep scheduler|grep -v grep|grep -v bash|awk '{print $2}'|xargs kill -9 """)

        c.run(
            '(source /etc/profile && nohup /opt/python35/bin/airflow webserver  >${AIRFLOW_HOME}/webserver.log  2>${AIRFLOW_HOME}/webserver.err &)  && sleep 1',
            pty=True)
        c.run(
            '(source /etc/profile && nohup /opt/python35/bin/airflow scheduler  >${AIRFLOW_HOME}/scheduler.log  2>${AIRFLOW_HOME}/scheduler.err &) && sleep 1 ',
            pty=True)

       

    def init_airflow3(self, conp):
        pass
        chrome_rpm=self.chrome_rpm
        chrome_driver=self.chrome_driver
        dags=self.dags
        tdir = '/root'
        c=Connection(conp[0], connect_kwargs={"password": conp[1]})
        c.put(chrome_rpm,tdir) 
        c.put(chrome_driver,tdir)
        c.run('yum install google-chrome-stable_current_x86_64.rpm -y')
        c.run('cp /root/chromedriver /opt/python35/bin')
        c.run('chmod 777 /opt/python35/bin/chromedriver')
        c.run('yum install mysql-devel -y')
        c.run('/opt/python35/bin/python3 -m pip install  zlsrc lmfscrap lmf zltask zlgp zlapp zlgp3 zlzz zlgg3 py3Fdfs  -i http://lanmengfei:since2015@10.0.64.25/pypi/simple --trusted-host 10.0.64.25')
       
   

# Airflow_cluster().install()
# Airflow_cluster().init_solt_pool()
def task():
    bg=time.time()
    jd_airflow(False).install()

    ed=time.time()
    cost=int(ed-bg)
    print("totally cost --%d s "%cost)

if __name__=='__main__':
    task()