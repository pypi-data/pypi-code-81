from fabric import Connection
from chtool.common.decorator import cost_time
from chtool.common.concurrency import threadpool

from invoke import Responder


class zookeeper():

    def __init__(self,source_dir,version="3.5.8"):
        self.source_dir=source_dir
        self.version = version
        self.target_dir="/root"
        self.prefix="/opt/zookeeper"
        self.redis_password="since2015"
        self.cfg=""

    def init_cfg(self,pin):

        self.cfg=f"""cat > {self.prefix}/conf/zoo.cfg << EOF {self.cfg}
dataDir={self.prefix}/data
dataLogDir={self.prefix}/logs
clientPort=2181
ticketTime=2000    
initLimit=10
syncLimit=5
server.1={pin[0][2]}:2888:3888
server.2={pin[1][2]}:2888:3888
server.3={pin[2][2]}:2888:3888
EOF"""


    def install(self,pin):


        def install_soft(conp):

            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            if self.source_dir:
                c.put(self.source_dir, self.target_dir)
            else:
                c.run(f'cd {self.target_dir} && wget https://mirror.bit.edu.cn/apache/zookeeper/zookeeper-{self.version}/apache-zookeeper-{self.version}-bin.tar.gz',encoding='utf-8')

            c.run(f'tar -zxvf /root/apache-zookeeper-{self.version}-bin.tar.gz -C /opt',encoding='utf-8')
            c.run(f'mv /opt/apache-zookeeper-{self.version}-bin {self.prefix}',encoding='utf-8')
            c.run(f"""echo  "export ZOOKEEPER_HOME={self.prefix}\nexport PATH=\$ZOOKEEPER_HOME/bin:\$PATH"  >> /etc/profile  && source /etc/profile""" , pty=True,encoding='utf-8')

            c.run(f'mkdir -p {self.prefix}/data')
            c.run(f'mkdir -p {self.prefix}/log')

            c.run(f'cp {self.prefix}/conf/zoo_sample.cfg {self.prefix}/conf/zoo.cfg')

            c.run(self.cfg)


        def install_cfg():
            num = 1
            for conp in pin:
                c = Connection(conp[0], connect_kwargs={"password": conp[1]})
                c.run(f"""echo "{num}" >  {self.prefix}/data/myid """)
                num += 1



        def install_start(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run(f'{self.prefix}/bin/zkServer.sh start')

        self.init_cfg(pin)

        for conp in pin:
            install_soft(conp)
        install_cfg()


        threadpool(pin,install_start).run(1)
        print('over')


if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]

    # conp=["root@172.16.16.5:22", "@jacky666", "seg1"]
    source_dir=r"C:\Users\Administrator\Desktop\lichanghua\apache-zookeeper-3.5.8-bin.tar.gz"
    # source_dir=False

    zookeeper(source_dir,version='3.5.8').install(pin)