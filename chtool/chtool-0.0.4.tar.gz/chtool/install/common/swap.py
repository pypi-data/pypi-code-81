from fabric import Connection

from invoke import Responder
import shutil
import os


def swap(conp, size=10240):
    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.run("dd if=/dev/zero of=/var/swap bs=1024 count=%dk" % size, pty=True)
    c.run("mkswap /var/swap", pty=True)
    c.run("mkswap -f /var/swap", pty=True)
    c.run("swapon /var/swap", pty=True)
    c.run("""echo "/var/swap  swap  swap defaults 0  0"  >>/etc/fstab  """, pty=True)


