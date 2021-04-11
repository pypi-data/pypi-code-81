from fabric import Connection
from chtool.common.concurrency import threadpool

# 配置/etc/hosts
def dns(pin):
    tmp = []
    for w in pin:
        ip = w[0][w[0].index("@") + 1:w[0].index(":")]
        name = w[2]
        tmp_str = "%s  %s" % (ip, name)
        tmp.append(tmp_str)
    myhosts = "\n".join(tmp)
    for w in pin:
        conp = w[:2]
        with Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120}) as c:
            c.run("sed -i '3,$d' /etc/hosts", pty=True) #删除从第2行开始的所有内容
            c.run("""echo "%s" >> /etc/hosts""" % myhosts, pty=True)

if __name__ == '__main__':
    pin = [
    ["root@172.16.16.4:22","@jacky666","seg3"],
    ["root@172.16.16.5:22","@jacky666","seg2"],
    ["root@172.16.16.6:22","@jacky666","seg1"]
    ]

    dns(pin)