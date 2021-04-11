from fabric import Connection

from invoke import Responder
import shutil
import os


def yum(conp):
    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.run("mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak", pty=True)

    ### 阿里云 yum 源
    c.run("curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo", pty=True)


