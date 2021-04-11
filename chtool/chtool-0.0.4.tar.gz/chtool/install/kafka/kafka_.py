from fabric import Connection
from chtool.common.decorator import cost_time
from chtool.common.concurrency import threadpool

from invoke import Responder


class kafka():

    def __init__(self,source_dir,version="3.5.8"):
        self.source_dir=source_dir
        self.version = version
        self.target_dir="/root"
        self.prefix="/opt/kafka"
        self.log_dir="\/opt\/kafka\/log"
        self.cfg=""

    def init_cfg(self,pin):

       pass

    def install(self,pin):


        def install_soft(conp):

            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            if self.source_dir:
                # c.put(self.source_dir, self.target_dir)
                pass
            else:
                # c.run(f'cd {self.target_dir} && wget https://mirror.bit.edu.cn/apache/zookeeper/zookeeper-{self.version}/apache-zookeeper-{self.version}-bin.tar.gz',encoding='utf-8')
                pass
            # c.run(f'tar -zxvf /root/kafka_{self.version}.tgz -C /opt',encoding='utf-8')
            # c.run(f'mv /opt/kafka_{self.version} {self.prefix}',encoding='utf-8')
            c.run(f'mkdir -p {self.log_dir}')

            c.run(f"""cp {self.prefix}/config/server.properties {self.prefix}/config/server.properties.bk""")

            c.run(f"""sed -i 's/#listeners=PLAINTEXT:\/\/:9092/listeners=PLAINTEXT:\/\/{conp[0].split('@')[1].split(":")[0]}:9092/g' {self.prefix}/config/server.properties""")
            c.run(f"""sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=localhost:2181/g' {self.prefix}/config/server.properties""")
            c.run(f"""sed -i 's/log.dirs=\/tmp\/kafka-logs/log.dirs={self.log_dir}/g' {self.prefix}/config/server.properties""")
            # c.run(f"""cat  's/delete.topic.enable=true/delete.topic.enable=true/g' {self.version}/config/server.properties""")

            # c.run(f'mkdir -p {self.prefix}/data')
            # c.run(f'mkdir -p {self.prefix}/log')
            #
            # c.run(f'cp {self.prefix}/conf/zoo_sample.cfg {self.prefix}/conf/zoo.cfg')
            #
            # c.run(self.cfg)


        def install_cfg():
            num = 1
            ips=[]
            for conp in pin:
                c = Connection(conp[0], connect_kwargs={"password": conp[1]})
                c.run(f"""sed -i 's/broker.id=0/broker.id={num}/g' {self.prefix}/config/server.properties""")
                num += 1
                ips.append(conp[0].split('@')[1].split(":")[0])

            for conp in pin:
                c = Connection(conp[0], connect_kwargs={"password": conp[1]})
                c.run(f"""sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect={ips[0]}:2181,{ips[1]}:2181,{ips[2]}:2181/g' {self.prefix}/config/server.properties""")


        def install_start(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run(f'{self.prefix}/bin/kafka-server-start.sh  -daemon {self.prefix}/config/server.properties')

        def install_stop(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run(f'{self.prefix}/bin/kafka-server-stop.sh ')

        def install_topic(conp,topic="test"):
            """
            #############################################################################################################
            /opt/kafka/bin/kafka-topics.sh --create --bootstrap-server 172.16.16.5:9092 --replication-factor 3 --partitions 3 --topic test

             bootstrap-server
             partitions指定topic分区数
             replication-factor指定topic每个分区的副本数


            #############################################################################################################
            /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server 172.16.16.5:9092


            #############################################################################################################
            /opt/kafka/bin/kafka-topics.sh --describe --bootstrap-server 172.16.16.5:9092  -topic test


            #############################################################################################################
            /opt/kafka/bin/kafka-topics.sh --delete --bootstrap-server 172.16.16.5:9092  -topic test


            #############################################################################################################
            """
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})

            ## 创建 topic
            # c.run(f'''{self.prefix}/bin/kafka-topics.sh --create --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 --replication-factor 3 --partitions 3 --topic {topic} ''')
            print(f'''{self.prefix}/bin/kafka-topics.sh --create --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 --replication-factor 3 --partitions 3 --topic {topic} ''')

            ## 查看已经创建的 topic
            # c.run(f"""{self.prefix}/bin/kafka-topics.sh --list --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 """)
            print(f"""{self.prefix}/bin/kafka-topics.sh --list --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 """)


            ## 查看 topic 详细信息
            # c.run(f"""{self.prefix}/bin/kafka-topics.sh --describe --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 """)
            print(f"""{self.prefix}/bin/kafka-topics.sh --describe --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092  -topic {topic} """)

            ##删除 topic
            # c.run(f"""{self.prefix}/bin/kafka-topics.sh --delete --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092 """)
            print(f"""{self.prefix}/bin/kafka-topics.sh --delete --bootstrap-server {conp[0].split('@')[1].split(":")[0]}:9092  -topic {topic} """)




        # self.init_cfg(pin)

        # for conp in pin:
            # install_soft(conp)
        # install_cfg()


        # threadpool(pin,install_start).run(1)
        # threadpool(pin,install_stop).run(1)

        install_topic(pin[1])

        print('over')


if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]

    # conp=["root@172.16.16.5:22", "@jacky666", "seg1"]
    source_dir=r"C:\Users\Administrator\Desktop\lichanghua\kafka_2.12-2.6.0.tgz"
    # source_dir=False

    kafka(source_dir,version='2.12-2.6.0').install(pin)