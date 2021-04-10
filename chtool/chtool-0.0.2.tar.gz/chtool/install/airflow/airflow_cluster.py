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

    def __init__(self, local_file_download=True):

        self.pin = [
            ["root@10.0.64.12:22", "BST@2020610", "airflow_master"],
            ["root@10.0.64.13:22", "BST@2020610", "airflow_worker1"],
            ["root@10.0.64.14:22", "BST@2020610", "airflow_worker2"],
            ["root@10.0.64.15:22", "BST@2020610", "airflow_worker3"],
            ["root@10.0.64.16:22", "BST@2020610", "airflow_worker4"],
            ["root@10.0.64.17:22", "BST@2020610", "airflow_worker5"],
            ["root@10.0.64.18:22", "BST@2020610", "airflow_worker6"],
            ["root@10.0.64.19:22", "BST@2020610", "airflow_worker7"],

        ]
        pin = self.pin
        self.airflow_db_pin = ["root@10.0.64.50:22", "BST@2020610", "airflow_db"]  ## airflow元数据库pin

        self.ip_pool_pin = ["root@10.0.64.19:22", "BST@2020610",
                            "airflow_worker7"]  ## 代理ip服务器主机配置 ， 默认 为 airflow worker7

        self.ip_pool_conp = ['postgres', 'since2015', '10.0.64.22', 'postgres',
                             'public']  ## 代理 ip 存放数据库配置 , 默认 为 爬虫中间库 db2

        airflow_db_pin = self.airflow_db_pin
        ip_pool_pin = self.ip_pool_pin
        ip_pool_conp = self.ip_pool_conp
        self.airflow_master = pin[0]
        self.airflow_wokers = pin[1:]
        self.airflow_cluster_pin = pin

        self.airflow_db = airflow_db_pin
        self.airflow_db_conp = ['postgres', 'since2015', re.findall('@(.+?):', airflow_db_pin[0])[0], 'postgres',
                                'public']

        self.redis_db = airflow_db_pin
        self.redis_db_conp = ['since2015', re.findall('@(.+?):', airflow_db_pin[0])[0]]

        self.ip_pool_pin = ip_pool_pin
        self.ip_pool_conp = ip_pool_conp

        self.airflow_setting = {'worker_concurrency': 18, 'workers': 8, 'parallelism': 180, 'max_threads': 50}

        self.oss_internal = True
        self.local_file_dir = "D:\\jingdong_airflowsys_download"
        self.local_file_download = local_file_download

        self.init_local_file()

    def init_local_file(self):
        tmpdir = self.local_file_dir

        self.redis_sdir = '%s\\redis-4.0.2.tar.gz' % tmpdir
        self.python_sdir = '%s\\Python-3.5.2.tgz' % tmpdir
        self.airmg_sdir = '%s\\airmg.sh' % tmpdir
        self.airflow_db_sdir = '%s\\postgresql-10.6-1-linux-x64.run' % tmpdir
        self.chrome_rpm = '%s\\google-chrome-stable_current_x86_64.rpm' % tmpdir
        self.chrome_driver = '%s\\chromedriver' % tmpdir
        self.dags = '%s\\dags.tar.gz' % tmpdir

    def down_webfile(self):
        tmpdir = self.local_file_dir
        if self.local_file_download:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            files = ['Python-3.5.2.tgz', 'airmg.sh',
                     'google-chrome-stable_current_x86_64.rpm', 'chromedriver', 'postgresql-10.6-1-linux-x64.run',
                     'redis-4.0.2.tar.gz', 'dags.tar.gz']
            m = oss(conp='')
            m.internal = self.oss_internal
            for file in files:
                bg = time.time()
                filename = 'backup/soft/' + file
                print(file)
                m.down_file(filename, "%s/%s" % (tmpdir, file))
                ed = time.time()
                cost = int(ed - bg)
                print("totoal cost --%d s " % cost)

    def install(self):
        self.down_webfile()
        self.init_common()  # 配置免密,dns
        self.install_python()  # 安装python
        self.install_pg()  # 安装 airflow 元数据库
        self.create_database()  # 在元数据库中 创建 airflow 数据库
        self.install_redis()  # 安装redis
        self.install_airflows()  # 安装 airflow
        self.init_airflows()  # 初始化 airflow 集群
        self.install_zlproxy()  # 配置 代理 ip 池
        self.init_solt_pool()  ## 配置airflow solt_pool
        self.init_cfg_host()

    def install_python(self):
        from lmfinstall.v2.python352 import install
        def f(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run('yum install -y patch')
            install(conp, self.python_sdir)

        mythread(f=f, arr=self.pin).run(len(self.pin))

    def init_common(self):
        from lmfinstall.common import hostname, dns, ssh
        hostname(self.airflow_cluster_pin)
        dns(self.airflow_cluster_pin)
        ssh(self.airflow_cluster_pin)

    def install_airflows(self):
        mythread(f=self.install_airflow, arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
        # for conp in self.airflow_cluster_pin:
        #     self.install_airflow(conp)

    def install_airflow(self, conp):

        pg_passwd = self.airflow_db_conp[1]
        pg_host = self.airflow_db_conp[2]
        redis_passwd = self.redis_db_conp[0]
        redis_host = self.redis_db_conp[1]
        worker_concurrency = self.airflow_setting['worker_concurrency']
        workers = self.airflow_setting['workers']
        parallelism = self.airflow_setting['parallelism']
        max_threads = self.airflow_setting['max_threads']

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
        c.run("useradd wk ", pty=True, warn=True)
        c.run("""sed -i 's/^executor = SequentialExecutor/executor = CeleryExecutor/g' /opt/airflow/airflow.cfg """)
        c.run(
            """sed -i 's/^result_backend = db.*airflow$/result_backend = db+postgresql:\/\/postgres:{pg_passwd}@{pg_host}\/airflow/g' /opt/airflow/airflow.cfg """.format(
                pg_passwd=pg_passwd, pg_host=pg_host))
        c.run(
            """sed -i 's/^broker_url = sqla.*airflow$/broker_url=redis:\/\/:{redis_passwd}@{redis_host}\/0/g' /opt/airflow/airflow.cfg """.format(
                redis_passwd=redis_passwd, redis_host=redis_host))
        c.run(
            """sed -i 's/^sql_alchemy_conn = sqlite.*airflow.db$/sql_alchemy_conn=postgresql:\/\/postgres:{pg_passwd}@{pg_host}\/airflow/g' /opt/airflow/airflow.cfg """.format(
                pg_passwd=pg_passwd, pg_host=pg_host))
        c.run("""sed -i 's/^default_timezone = utc/default_timezone = Asia\/Shanghai/g' /opt/airflow/airflow.cfg """)
        c.run(
            """sed -i 's/^worker_concurrency = [0-9]*$/worker_concurrency = {worker_concurrency}/g' /opt/airflow/airflow.cfg """.format(
                worker_concurrency=worker_concurrency))
        c.run(
            """sed -i 's/^workers = [0-9]*$/workers = {workers}/g' /opt/airflow/airflow.cfg """.format(workers=workers))
        c.run("""sed -i 's/^parallelism = [0-9]*$/parallelism = {parallelism}/g' /opt/airflow/airflow.cfg """.format(
            parallelism=parallelism))
        c.run("""sed -i 's/^max_threads = [0-9]*$/max_threads = {max_threads}/g' /opt/airflow/airflow.cfg """.format(
            max_threads=max_threads))
        c.run("""sed -i 's/^load_examples = True/load_examples = False/g' /opt/airflow/airflow.cfg """)
        c.run("""sed -i 's/^catchup_by_default = True/catchup_by_default = False/g' /opt/airflow/airflow.cfg """)

    def install_pg(self):

        from lmfinstall.postgresql.postgresql1061 import install, plpython

        conp = self.airflow_db

        pgdata = '/opt/PostgreSQL/10/data'
        install(conp, self.airflow_db_sdir, plpython="plpython35")
        c = Connection(conp[0], connect_kwargs={"password": conp[1]})

        c.run("""sed -i 's/^max_connections = [0-9]*/max_connections = 500/g' %s/postgresql.conf""" % pgdata, pty=True)
        c.run("""systemctl restart postgresql-10.service""", pty=True)

    def install_redis(self):
        conp = self.redis_db
        tdir = '/root'
        c = Connection(conp[0], connect_kwargs={"password": conp[1]})
        c.put(self.redis_sdir, tdir)
        c.run('tar -zxvf  /root/redis-4.0.2.tar.gz')
        c.run('cd /root/redis-4.0.2 && make && make install')
        c.run('cp /root/redis-4.0.2/redis.conf /usr/local/bin')
        c.run("""sed -i 's/^# requirepass foobared/requirepass since2015/g' /usr/local/bin/redis.conf""")
        c.run("""sed -i 's/^bind 127.0.0.1/# bind 127.0.0.1/g' /usr/local/bin/redis.conf""")
        result = c.run('firewall-cmd --state', pty=True, warn=True, hide=True, encoding='utf8')
        if 'not running' not in result.stdout:
            c.run("""firewall-cmd --permanent --zone=public --add-port=6379/tcp && firewall-cmd --reload""")

        c.run("""nohup /usr/local/bin/redis-server /usr/local/bin/redis.conf &> /usr/local/bin/redis.log &""")

    def restore_database(self):
        pass

    def init_solt_pool(self):
        sql = """INSERT INTO slot_pool (id, pool, slots, description) VALUES (1, 'abc_a1', 28, ''),(2, 'abc_a2', 22, ''),
        (3, 'abc_a3', 30, ''),(4, 'abc_a4', 15, ''),(5, 'abc_b', 10, ''),(6, 'abc_shenpi', 10, ''),(7, 'abc_zljzsheng', 20, ''),
        (8, 'abc_zlsys', 10, ''),(9, 'abc_c', 5, ''),(10, 'abc_d', 5, ''),(11, 'abc_jianzhu', 6, ''),(12, 'abc_yszz', 4, ''),
        (13, 'abc_zlqy', 5, ''),(14, 'abc_zizhixx', 10, '');"""

        conp = self.airflow_db_conp
        db_name = 'airflow'

        con = psycopg2.connect(database=db_name, user=conp[0], password=conp[1], host=conp[2])
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()


def init_cfg_host(self):
    sql = """ update cfg set host = '10.0.64.21' where host = '192.168.4.198';
                update cfg set host = '10.0.64.22' where host = '192.168.4.199';
                update cfg set host = '10.0.64.23' where host = '192.168.4.200';
                update cfg set host = '10.0.64.24' where host = '192.168.4.201';
                update cfg set get_ip_url='http://10.0.64.19/random'; """

    conp = ['postgres', 'since2015', "10.0.64.24", 'postgres', 'public']
    con = psycopg2.connect(database=db_name, user=conp[0], password=conp[1], host=conp[2])
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()


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
    mythread(f=self.init_airflow1, arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
    mythread(f=self.init_airflow2, arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
    mythread(f=self.init_airflow3, arr=self.airflow_cluster_pin).run(len(self.airflow_cluster_pin))
    # for conp in self.airflow_cluster_pin:
    #     self.init_airflow1(conp)
    # for conp in self.airflow_cluster_pin:
    #     self.init_airflow2(conp)
    # for conp in self.airflow_cluster_pin:
    #     self.init_airflow3(conp)


def init_airflow1(self, conp):
    wktdir = '/home/wk'
    roottdir = '/root'

    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.put(self.airmg_sdir, wktdir)
    c.run('chmod 777 %s/airmg.sh' % wktdir)
    c.run('chown wk: %s/airmg.sh' % wktdir)
    c.run('yum -y install nfs-utils rpcbind')
    pgasw1 = Responder("New password:", "wk\n")
    pgasw2 = Responder("Retype new password:", "wk\n")

    c.run('passwd wk', watchers=[pgasw1, pgasw2], pty=True)
    c.put(self.airmg_sdir, roottdir)
    c.run('chmod 777 %s/airmg.sh' % roottdir)
    c.run('chmod 777 -R /opt/airflow')
    if conp == self.airflow_master:

        c.run('source /etc/profile && /opt/python35/bin/airflow initdb')

        c.run('mkdir -p /opt/airflow/dags')
        c.run('systemctl start nfs-server')
        c.run('systemctl enable nfs-server')
        c.run('> /etc/exports')
        c.run('echo "/opt/airflow/dags {master_ip}/24(rw,sync,no_root_squash)" >> /etc/exports'.format(master_ip=
                                                                                                       re.findall(
                                                                                                           '@(.+?):',
                                                                                                           self.airflow_master[
                                                                                                               0])[
                                                                                                           0].rsplit(
                                                                                                           '.',
                                                                                                           maxsplit=1)[
                                                                                                           0] + '.0'))
        c.run('exportfs -r')
        result = c.run('firewall-cmd --state', pty=True, warn=True, hide=True, encoding='utf8')

        if 'not running' not in result.stdout:
            c.run('firewall-cmd --permanent --zone=public --add-port=111/tcp')
            c.run('firewall-cmd --permanent --zone=public --add-port=2049/tcp')
            c.run('firewall-cmd --reload')
    else:

        c.run('mkdir -p /opt/airflow/dags')
        c.run('systemctl start rpcbind.service')
        c.run('systemctl enable rpcbind.service')
        std = c.run('df -h', hide=True).stdout
        if 'airflow' in std:
            c.run('umount -d /opt/airflow/dags')
        c.run('mount -t nfs {master_ip}:/opt/airflow/dags /opt/airflow/dags'.format(
            master_ip=re.findall('@(.+?):', self.airflow_master[0])[0]), pty=True)


def init_airflow2(self, conp):
    pass_wk = 'wk'

    if conp == self.airflow_master:
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

    else:
        c = Connection(re.sub('root', 'wk', conp[0]), connect_kwargs={"password": pass_wk})  # 切换 普通 用户
        otwk = c.run(
            """ ps -ef |grep -E 'celery|serve_logs'|grep -v grep|grep -v bash|awk '{print $2}'|wc -l """,
            hide=True).stdout
        if int(otwk) > 0:
            c.run(
                """ ps -ef |grep -E 'celery|serve_logs'|grep -v grep|grep -v bash|awk '{print $2}'|xargs kill -9 """)
        print(conp)
        c.run(
            '(source /etc/profile && nohup /opt/python35/bin/airflow  worker  >${AIRFLOW_HOME}/worker.log  2>${AIRFLOW_HOME}/worker.err & ) && sleep 1',
            pty=True)


def init_airflow3(self, conp):
    pass
    chrome_rpm = self.chrome_rpm
    chrome_driver = self.chrome_driver
    dags = self.dags
    tdir = '/root'
    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.put(chrome_rpm, tdir)
    c.put(chrome_driver, tdir)
    c.run('yum install google-chrome-stable_current_x86_64.rpm -y')
    c.run('cp /root/chromedriver /opt/python35/bin')
    c.run('chmod 777 /opt/python35/bin/chromedriver')
    c.run('yum install mysql-devel -y')
    c.run(
        '/opt/python35/bin/python3 -m pip install zlproxy zlsrc lmfscrap lmf zltask zlgp zlapp zlgp3 zlzz zlgg3 py3Fdfs  -i https://jacky:Jacky666.@www.zhulong.com.cn/pypi/simple')
    if conp == self.airflow_master:
        c.put(dags, tdir)
        c.run('tar -zxvf /root/dags.tar.gz -C /opt/airflow/dags')
        ###ext
        c.run("""sed -i 's/"loc":"aliyun"/"loc":"jdyun"/g' /opt/airflow/dags/DB_A/*.py""")
        c.run("""sed -i 's/"loc":"aliyun"/"loc":"jdyun"/g' /opt/airflow/dags/DB_B/*.py""")
        c.run("""sed -i 's/"loc":"aliyun"/"loc":"jdyun"/g' /opt/airflow/dags/DB_C/*.py""")
        c.run("""sed -i 's/"loc":"aliyun"/"loc":"jdyun"/g' /opt/airflow/dags/DB_D/*.py""")


def install_zlproxy(self):
    conp = self.ip_pool_pin
    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.run(
        '/opt/python35/bin/python3 -m pip install zlproxy -i https://jacky:Jacky666.@www.zhulong.com.cn/pypi/simple')
    c.run('yum install nginx -y')
    c.run('mkdir -p /var/www/zlproxy')
    c.run('mkdir -p /var/www/zlproxy/scrap')

    c.run('''cat > /var/www/zlproxy/uwsgi.ini << EOF
[uwsgi]
module = run:app
master = true
processes = 8
chdir = /var/www/zlproxy/
socket = /var/www/zlproxy/uwsgi.sock
socket = 127.0.0.1:5000
logto = /var/www/zlproxy/uwsgi.log
logto2 = /var/www/zlproxy/uwsgierror.log
chmod-socket = 660
vacuum = true
listen=2048
max-requests = 10000
thunder-lock = true
log-maxsize = 50000000
pidfile=%(chdir)/uwsgi.pid
stats=%(chdir)/uwsgi.status
EOF
    ''')
    c.run('''cat > /var/www/zlproxy/nginx.conf << EOF
worker_processes 8;
worker_rlimit_nofile 20000;
error_log  /var/www/zlproxy/nginx_error.log  error;
events { worker_connections 1024; use epoll; }
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    server {
         listen 80;
         location / {
            include /etc/nginx/uwsgi_params;
            uwsgi_pass 127.0.0.1:5000;
         }
    }

}
EOF
    ''')

    c.run('''cat > /var/www/zlproxy/scrap/ip_pool_run.py << EOF
from zlproxy.scheduler import Scheduler

if __name__ == '__main__':
    scheduler=Scheduler()
    scheduler.run()
EOF
    ''')
    c.run('''cat > /var/www/zlproxy/run.py << EOF
from zlproxy.flask_api import app

if __name__=="main":
    app.run()
EOF
    ''')
    c.run("""cat > /etc/sysctl.conf << EOF
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).

kernel.shmmax = 500000000
kernel.shmmni = 4096
kernel.shmall = 4000000000
kernel.sem = 500 1024000 200 4096
kernel.sysrq = 1
kernel.core_uses_pid = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.msgmni = 2048

net.core.somaxconn = 20480  
net.core.rmem_default = 262144
net.core.wmem_default = 262144
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 4096 16777216
net.ipv4.tcp_wmem = 4096 4096 16777216
net.ipv4.tcp_mem = 786432 2097152 3145728
net.ipv4.tcp_max_syn_backlog = 16384
net.core.netdev_max_backlog = 20000
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_tw_reuse = 1 
net.ipv4.tcp_tw_recycle = 1 
net.ipv4.tcp_max_orphans = 131072
net.ipv4.tcp_syncookies = 0

EOF""", pty=True, encoding='utf8')
    c.run("sysctl -p", pty=True)
    c.run("""cat > /etc/security/limits.conf <<EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 131072
* hard nproc 131072
EOF
    """, pty=True, encoding='utf8')

    ip_db = self.ip_pool_conp[2]
    c.run(
        '''sed -i "s/^PG_HOST = '.*'/PG_HOST = '{ip_db}'/g" /opt/python35/lib/python3.5/site-packages/zlproxy/setting.py'''.format(
            ip_db=ip_db))
    sql = '''create  schema if not exists ips'''
    db_command(sql, dbtype='postgresql', conp=self.ip_pool_conp)

    c.run("""/opt/python35/bin/python3 -c 'from zlproxy.db import PGClient;PGClient().create()'""")  ## 创建 proxy 表
    c.run(
        'nohup /opt/python35/bin/python3 -u /var/www/zlproxy/scrap/ip_pool_run.py 1> /var/www/zlproxy/scrap/success.log 2> /var/www/zlproxy/scrap/error.log &')  # 启动 ip 服务
    c.run('nohup /opt/python35/bin/uwsgi --ini /var/www/zlproxy/uwsgi.ini &')  # 启动 uwsgi 服务
    c.run('nginx -c /var/www/zlproxy/nginx.conf')  # 启动nginx


# Airflow_cluster().install()
# Airflow_cluster().init_solt_pool()
def task():
    bg = time.time()
    jd_airflow(False).install()

    ed = time.time()
    cost = int(ed - bg)
    print("totally cost --%d s " % cost)


if __name__ == '__main__':
    task()