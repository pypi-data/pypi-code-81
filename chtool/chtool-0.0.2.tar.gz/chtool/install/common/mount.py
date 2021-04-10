from fabric import Connection

def mount(conp, k, v):
    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.run("umount %s " % k, pty=True, warn=True)

    c.run("mkfs -t ext4 %s" % k, pty=True)

    c.run("mkdir -p %s" % v, pty=True)

    c.run("mount %s %s" % (k, v), pty=True, warn=True)

    k1 = k.replace("/", '\/')
    c.run("sed -i '/%s/d' /etc/fstab" % k1, pty=True)

    c.run("echo '%s %s  ext4 defaults 0 0'>> /etc/fstab " % (k, v), pty=True)


