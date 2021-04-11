from fabric import Connection
from chtool.common.decorator import cost_time
from chtool.common.concurrency import threadpool

from invoke import Responder


class elasticsearch():

    def __init__(self,source_dir,version="3.5.8"):
        self.source_dir=source_dir
        self.version = version
        self.target_dir="/root"
        self.prefix="/opt/elasticsearch"
        self.log_dir="\/data\/es\/log"
        self.data_dir="\/data\/es\/data"
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
            # c.run(f'tar -zxvf  /root/elasticsearch-{self.version}.tar.gz -C /opt',encoding='utf-8')
            # c.run(f'mv /opt/elasticsearch-{self.version} {self.prefix}',encoding='utf-8')

            c.run(f'mkdir -p {self.log_dir}')
            c.run(f'mkdir -p {self.data_dir}')

            c.run('useradd elk')
            c.run(f'chown elk -R {self.prefix}')
            c.run(f'chown elk -R {self.log_dir}')
            c.run(f'chown elk -R {self.data_dir}')

            c.run(f"""cp {self.prefix}/config/jvm.options {self.prefix}/config/jvm.options.bk""")
            c.run(f"""cp {self.prefix}/config/elasticsearch.yml {self.prefix}/config/elasticsearch.yml.bk""")
            #
            c.run(f"""sed -i 's/-Xms1g/-Xms512m/g' {self.prefix}/config/jvm.options""")
            c.run(f"""sed -i 's/-Xmx1g/-Xmx512m/g' {self.prefix}/config/jvm.options""")
            c.run(f"""sed -i 's/#cluster.name: my-application/cluster.name: my-es/g' {self.prefix}/config/elasticsearch.yml""")
            c.run(f"""sed -i 's/#path.data: \/path\/to\/data/path.data: {self.data_dir}/g' {self.prefix}/config/elasticsearch.yml""")
            c.run(f"""sed -i 's/#path.logs: \/path\/to\/logs/path.logs: {self.log_dir}/g' {self.prefix}/config/elasticsearch.yml""")
            c.run(f"""sed -i 's/#network.host: 192.168.0.1/network.host: 0.0.0.0/g' {self.prefix}/config/elasticsearch.yml""")
            c.run(f"""sed -i 's/#bootstrap.memory_lock: true/bootstrap.memory_lock: true/g' {self.prefix}/config/elasticsearch.yml""")
            c.run("""cat > /etc/security/limits.conf <<EOF
* soft nofile 524288
* hard nofile 524288
* soft nproc 131072
* hard nproc 131072
* soft memlock unlimited
* hard memlock unlimited
EOF""", pty=True, encoding='utf8')
            c.run("""cat > /etc/sysctl.conf <<EOF
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
vm.swappiness = 1
vm.zone_reclaim_mode = 0
vm.dirty_expire_centisecs = 500
vm.dirty_writeback_centisecs = 100
vm.dirty_background_ratio = 0 # See Note 5
vm.dirty_ratio = 0
vm.dirty_background_bytes = 1610612736
vm.dirty_bytes = 4294967296
vm.max_map_count = 262144
EOF """ ,pty=True, encoding='utf8')
            c.run('sysctl -p')



        def install_cfg():
            num = 1
            ips=[]
            for conp in pin:
                c = Connection(conp[0], connect_kwargs={"password": conp[1]})
                c.run(f"""sed -i 's/#node.name: node-1/node.name: node-{num}/g' {self.prefix}/config/elasticsearch.yml""")
                num += 1
                ips.append(conp[0].split('@')[1].split(":")[0])

            for conp in pin:
                c = Connection(conp[0], connect_kwargs={"password": conp[1]})
                c.run(f"""sed -i 's/#discovery.zen.ping.unicast.hosts: \["host1", "host2"\]/discovery.zen.ping.unicast.hosts: \["{ips[0]}", "{ips[1]}","{ips[2]}"\]/g' {self.prefix}/config/elasticsearch.yml""")

        def install_start(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})
            c.run(f'su elk -c "{self.prefix}/bin/elasticsearch -d"')

        def install_stop(conp):
            c = Connection(conp[0], connect_kwargs={"password": conp[1]})



        # self.init_cfg(pin)
        #
        # for conp in pin:
        #     install_soft(conp)
        install_cfg()


        # threadpool(pin,install_start).run(1)
        # threadpool(pin,install_stop).run(1)


        print('over')


if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]

    # conp=["root@172.16.16.5:22", "@jacky666", "seg1"]
    source_dir=r"C:\Users\Administrator\Desktop\lichanghua\elasticsearch-6.7.0.tar.gz"
    # source_dir=False

    elasticsearch(source_dir,version='6.7.0').install(pin)