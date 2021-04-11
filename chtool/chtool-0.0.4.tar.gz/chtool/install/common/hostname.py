from fabric import Connection
from chtool.common.concurrency import threadpool

# 给计算机命名
def hostname(pin):
    """
    给计算机命名
    """
    def hostname_single(w):
        conp = w[:2]
        name = w[2]
        with Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120}) as c:
            c.run("hostnamectl --static set-hostname %s" % name, pty=True)

    threadpool(pin,hostname_single).run(1)





if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]
    hostname(pin)