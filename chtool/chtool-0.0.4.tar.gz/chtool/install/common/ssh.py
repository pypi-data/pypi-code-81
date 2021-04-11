from fabric import Connection

from invoke import Responder
import shutil
import os




def ssh(pin, user='root'):
    # user='lmf'
    for conp in pin:
        with Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120}) as c:

            if c.run("""egrep "^%s" /etc/passwd""" % user, warn=True, pty=True).failed:
                c.run("useradd  %s " % user, pty=True)

            if user == 'root':
                c.run("""ssh-keygen -t rsa  -m PEM  -b 4096 -P '' -f /root/.ssh/id_rsa  """, pty=True,
                      watchers=[Responder("Overwrite", "y\n")])
            else:
                c.run(
                    """sudo -u %s ssh-keygen -t rsa  -m PEM  -b 4096 -P '' -f /home/%s/.ssh/id_rsa  """ % (user, user),
                    pty=True, watchers=[Responder("Overwrite", "y\n")])
            tmpdir = '/tmp/tmp1'
            tmpdir1 = '/tmp'
            if not os.path.exists(tmpdir1):
                os.mkdir(tmpdir1)
            if not os.path.exists(tmpdir):
                os.mkdir(tmpdir)
            if user == 'root':
                c.get("/root/.ssh/id_rsa.pub", "%s/id_rsa.pub.%s" % (tmpdir, conp[2]))
            else:
                c.get("/home/%s/.ssh/id_rsa.pub" % user, "%s/id_rsa.pub.%s" % (tmpdir, conp[2]))

    farr = os.listdir(tmpdir)
    with open(tmpdir + '/authorized_keys', 'w') as f:
        for w in farr:
            file = tmpdir + "/" + w
            if w.startswith('id_rsa'):
                with open(file, 'r') as f1:
                    content = f1.read()
                f.write(content + "\n")

    for conp in pin:
        c = Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120})
        if user == "root":
            c.put(tmpdir + '/authorized_keys', "/root/.ssh/")
            c.run("chmod -R 700 /root/.ssh/authorized_keys")

        else:
            c.put(tmpdir + '/authorized_keys', "/home/%s/.ssh/" % user)
            c.run("chmod -R 700 /home/%s/.ssh/authorized_keys" % user)
            c.run("chown -R %s:%s /home/%s/.ssh/authorized_keys" % (user, user, user))
    for conp in pin:
        c = Connection(conp[0], connect_kwargs={"password": conp[1], "banner_timeout": 120})
        if user == 'root':
            cmd="ssh-keyscan -t rsa,dsa -H %s %s >  /root/.ssh/known_hosts" % (
            ' '.join([w[0][w[0].index('@') + 1:w[0].index(':')] for w in pin]), ' '.join([w[2] for w in pin]))

        else:
            cmd = """sudo -u %s ssh-keyscan -t rsa,dsa -H %s %s > /home/%s/.ssh/known_hosts """ % (
            user, ' '.join([w[0][w[0].index('@') + 1:w[0].index(':')] for w in pin]),
            ' '.join([w[2] for w in pin])
            , user)
        print(cmd)
        c.run(cmd)

    shutil.rmtree(tmpdir)


if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]
    ssh(pin)