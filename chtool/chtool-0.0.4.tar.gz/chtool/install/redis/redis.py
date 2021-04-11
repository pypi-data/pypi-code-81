from fabric import Connection
from chtool.common.decorator import cost_time
from chtool.common.concurrency import threadpool

from invoke import Responder


class redis():

    def __init__(self,source_dir,version="6.0.9"):
        self.source_dir=source_dir
        self.version = version
        self.target_dir="/root"
        self.prefix="/usr/local/"
        self.redis_password="since2015"

    def install(self,conp):

        c = Connection(conp[0], connect_kwargs={"password": conp[1]})

        if self.source_dir:
            c.put(self.source_dir, self.target_dir)
        else:
            c.run(f'cd {self.target_dir} && wget http://download.redis.io/releases/redis-{self.version}.tar.gz',encoding='utf-8')

        c.run(f'tar -zxvf  /root/redis-{self.version}.tar.gz')

        c.run("yum install lrzsz  openssl-devel  zlib-devel  sqlite-devel gcc nfs-utils readline-devel tcl -y ",encoding='utf-8')
        ## redis 6 版本以上需使用 gcc版本 > 5.3 以上编译 , centos7 默认安装 gcc 为 4.8
        ##升级 gcc
        c.run('yum -y install centos-release-scl',encoding='utf-8')
        c.run('yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils',encoding='utf-8')

        #### c.run(f'scl enable devtoolset-9 bash && cd /root/redis-{self.version} && make &&make install') #scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本

        c.run('echo "source /opt/rh/devtoolset-9/enable" >> /etc/profile',encoding='utf-8')

        c.run(f'source /etc/profile && cd /root/redis-{self.version} && make distclean &&make install',encoding='utf-8')

        c.run(f'cp /root/redis-{self.version}/redis.conf /usr/local/bin',pty=True,encoding='utf-8')
        c.run(f"""sed -i 's/^# requirepass foobared/requirepass {self.redis_password}/g' /usr/local/bin/redis.conf""",pty=True,encoding='utf-8')
        c.run("""sed -i 's/^bind 127.0.0.1/# bind 127.0.0.1/g' /usr/local/bin/redis.conf""",pty=True,encoding='utf-8')
        result = c.run('firewall-cmd --state', pty=True, warn=True, hide=True, encoding='utf8')
        if 'not running' not in result.stdout:
            c.run("""firewall-cmd --permanent --zone=public --add-port=6379/tcp && firewall-cmd --reload""",pty=True,encoding='utf-8')

        c.run("""nohup /usr/local/bin/redis-server /usr/local/bin/redis.conf &> /usr/local/bin/redis.log &""",pty=True,encoding='utf-8')

if __name__ == '__main__':
    conp=["root@172.16.16.5:22", "@jacky666", "seg1"]
    source_dir=r"C:\Users\Administrator\Desktop\lichanghua\redis-6.0.9.tar.gz"
    # source_dir=False

    redis(source_dir,version='6.0.9').install(conp)