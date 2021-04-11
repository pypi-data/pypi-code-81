from fabric import Connection
from chtool.common import threadpool
from invoke import Responder
import shutil
import os


def java(conp, source_path, **krg):

    c = Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120})

    para = {
        "target_path": "/root"
    }

    para.update(krg)
    target_path = para['target_path']
    c.put(source_path, target_path)

    c.run("yum remove jdk -y", pty=True, warn=True, encoding='utf8')
    c.run("yum install -y /root/jdk-8u271-linux-x64.rpm", pty=True, encoding='utf8')
    c.run("""sed -i '/JAVA_HOME=\\/usr\\/java/d'  /etc/profile  """, encoding='utf8')
    c.run("""sed -i '/JAVA_HOME\\/bin/d'  /etc/profile  """, encoding='utf8')
    c.run("""sed -i '/CLASSPATH=.:\$JAVA_HOME\\/lib\\/dt.jar/d'  /etc/profile  """, encoding='utf8')
    c.run(
        """echo "export JAVA_HOME=/usr/java/jdk1.8.0_271\nexport PATH=\$JAVA_HOME/bin:\$PATH\nexport CLASSPATH=.:\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar" >> /etc/profile"""
        , pty=True, encoding='utf8')
    c.run("source  /etc/profile")

if __name__ == '__main__':
    source_path=r'C:\Users\Administrator\Desktop\lichanghua\jdk-8u271-linux-x64.rpm'
    pin = [
    ["root@172.16.16.4:22","@jacky666","seg3"],
    ["root@172.16.16.5:22","@jacky666","seg2"],
    ["root@172.16.16.6:22","@jacky666","seg1"]
    ]

    pin=[i for i in zip(pin,[source_path]*3)]
    print(pin)
    # java(conp,source_path=source_path)
    threadpool(pin,java,var_type='double').run(1)
