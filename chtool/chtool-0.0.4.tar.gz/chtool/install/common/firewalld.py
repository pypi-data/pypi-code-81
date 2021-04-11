from fabric import Connection

from invoke import Responder
import shutil
import os

from chtool.common import threadpool


def firewalld(conp):
    """

    ####################################################################################################################################
        SELinux : 部署在 Linux 上用于增强系统安全的功能模块

        传统的 Linux 系统中，默认权限是对文件或目录的所有者、所属组和其他人的读、写和执行权限进行控制，这种控制方式称为自主访问控制（DAC）方式；
        而在 SELinux 中，采用的是强制访问控制（MAC）系统，也就是控制一个进程对具体文件系统上面的文件或目录是否拥有访问权限，而判断进程是否可以访问文件或目录的依据

        setenforce 命令只能让 SELinux 在 enforcing 和 permissive 两种模式之间进行切换。如果从启动切换到关闭，或从关闭切换到启动，则只能修改配置文件
        setenforce 0  切换成 permissive（宽容模式）
        setenforce 1  切换成 enforcing（强制模式）
                            disabled（不生效）

        如果从强制模式（enforcing）、宽容模式（permissive）切换到关闭模式（disabled），或者从关闭模式切换到其他两种模式，则必须重启 Linux 系统才能生效，
        但是强制模式和宽容模式这两种模式互相切换不用重启 Linux 系统就可以生效
        http://c.biancheng.net/view/1147.html
    #####################################################################################################################################


    #########################################################
        firewalld
         参数解释
         1、firwall - cmd：是Linux提供的操作firewall的一个工具；
         2、--permanent：表示设置为持久；
         3、--add - port：标识添加的端口；
    #########################################################


    """

    c = Connection(conp[0], connect_kwargs={"password": conp[1]})
    c.run("systemctl stop firewalld && sudo systemctl disable firewalld", pty=True)
    c.run("sed -ri s/SELINUX=enforcing/SELINUX=disabled/g /etc/selinux/config", pty=True) #关闭selinux安全增强
    # c.run("setenforce 0", pty=True)



    # result=c.run('systemctl status firewalld',pty=True, warn=True, hide=True, encoding='utf8')
    # result=c.run('firewall-cmd --state',pty=True, warn=True, hide=True, encoding='utf8')
    # print(result)
    # c.run('service firewalld restart',pty=True,encoding='utf-8') #重启
    # c.run('service firewalld start',encoding='utf-8') #开启
    c.run('service firewalld stop',encoding='utf-8') #关闭

    # result=c.run('firewall-cmd --query-port=8080/tcp',pty=True, warn=True, hide=True, encoding='utf8') #查询端口是否开放
    # print(result)

    # c.run('firewall-cmd --permanent --add-port=80/tcp',pty=True,encoding='utf-8') #开放端口
    # c.run('firewall-cmd --permanent --remove-port=80/tcp',pty=True,encoding='utf-8') #移除端口
    # c.run('firewall-cmd --reload',pty=True,encoding='utf-8') #重启防火墙(修改配置后要重启防火墙)



if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]

    # threadpool(pin,yum).run(1)
    # threadpool(pin, firewalld).run(1)
    for conp in pin:
        firewalld(conp)