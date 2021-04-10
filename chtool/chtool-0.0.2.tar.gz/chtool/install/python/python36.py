from fabric import Connection
from chtool.common.decorator import cost_time
from chtool.common.concurrency import threadpool

from invoke import Responder


class python():
    def __init__(self,source_dir,version="3.6.8"):
        self.source_dir=source_dir
        self.version = version
        self.target_dir="/tmp/pythoninstall"
        self.prefix="/opt/python36"
        self.enableshared=True


    @cost_time
    def install(self,pin,num=2):

        threadpool(pin,self.install_single).run(num)


    def install_single(self,conp):

        with Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120}) as c:
            source_dir = self.source_dir
            target_dir = self.target_dir
            prefix=self.prefix
            version=self.version

            if c.run("test -f %s" % source_dir, warn=True).failed:
                c.run("mkdir -p %s" % target_dir)
            if c.run(f"test -f {target_dir}/Python-{version}.tgz", pty=True, warn=True).failed:
                print("上传pthon压缩包")
                c.put(source_dir, target_dir)

            c.run("yum install lrzsz  openssl-devel  zlib-devel  sqlite-devel gcc nfs-utils readline-devel -y ",encoding='utf-8')
            c.run(f"tar -zxvf {target_dir}/Python-{version}.tgz -C /root", pty=True,encoding='utf-8')

            if self.enableshared:
                # 启动共享编译，方便其他程序调用python
                c.run(f"cd /root/Python-{version} && ./configure --prefix={prefix} --enable-shared && make && make install",pty=True,encoding='utf-8')
                if c.run("test -f /usr/lib64/libpython3.6m.so.1.0", warn=True).failed:
                    c.run("ln -s /opt/python36/lib/libpython3.6m.so.1.0  /usr/lib64/libpython3.6m.so.1.0", pty=True,encoding='utf-8')

            else:
                c.run(f"cd /root/Python-{version} && ./configure --prefix={prefix}  && make && make install" , pty=True,encoding='utf-8')

            prefix1 = prefix.replace('/', '\\/')
            c.run(f"""sed -i '/{prefix1}\\/bin/d'  /etc/profile""", pty=True, warn=True,encoding='utf-8')
            c.run(f"""echo  "export PATH=\$PATH:{prefix}/bin"  >> /etc/profile  && source /etc/profile""" , pty=True,encoding='utf-8')

            c.run('yum install -y patch',pty=True,encoding='utf-8')
            c.run(f"{prefix}/bin/python3 -m pip install readline -i https://pypi.douban.com/simple  " , pty=True,encoding='utf-8')
            c.run(f"{prefix}/bin/python3 -m pip install --upgrade pip  -i https://pypi.douban.com/simple  ", pty=True,encoding='utf-8')


if __name__ == '__main__':
    source_dir=r'C:\Users\Administrator\Desktop\lichanghua\Python-3.6.8.tgz'
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]

    python(source_dir).install(pin,num=3)
