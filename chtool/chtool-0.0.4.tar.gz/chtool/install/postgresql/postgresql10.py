from fabric import Connection

from invoke import Responder
import os


# 安装 postgresql-10.6-1-linux-x64.run
# pg安装平台是 centos 7.3
# 测试在win7 上运程为cent7.3 安装 postgresql-10.6-1-linux-x64.run 成功


# postgresql的安装教程
# postgresql 分为软件部分 和数据目录部分
# 常见目录
# /opt/PostgreSQL/10
# /opt/PostgreSQL/10/data
# /PGDATA/pg_hba.conf 控制访问
# /PGDATA/postgresql.conf 是数据库配置

class postgresql():
    def __init__(self):
        pass

    def install(self,conp, spath, **krg):

        c = Connection(conp[0], connect_kwargs={"password": conp[1]})

        print("Ensure that the installed file must be postgresql-10.6-1-linux-x64.run !")

        para = {
            "spath": spath,
            "tpath": "/root/lmfinstall/postgresql-10.6",
            "pgdata": "",
            "plpython": "plpython34"
        }

        para.update(krg)
        print(para.keys())
        sdir = para["spath"]
        tdir = para["tpath"]
        pgdata = para["pgdata"]
        con = c

        # /pgdownlaod/postgresql-10.6-1-linux-x64.run 在window上相当于终端所在盘X:/pgdownlaod/postgresql-10.6-1-linux-x64.run
        if con.run("test -f %s" % tdir, warn=True).failed:
            con.run("mkdir -p %s" % tdir)

        con.put(sdir, tdir)
        con.run("chmod +x %s/postgresql-10.6-1-linux-x64.run" % tdir)
        pgasw1 = Responder("Installation Directory", "\n")
        pgasw2 = Responder("PostgreSQL Server \[Y/n\]", "y\n")
        pgasw3 = Responder("pgAdmin 4 \[Y/n\]", "n\n")
        pgasw4 = Responder("Stack Builder \[Y/n\]", "y\n")
        pgasw5 = Responder("Command Line Tools \[Y/n\]", "y\n")
        pgasw6 = Responder("Is the selection above correct", "y\n")
        pgasw7 = Responder("Data Directory ", "%s\n" % pgdata)
        pgasw8 = Responder("Password ", "since2015\n")
        pgasw9 = Responder("Retype password", "since2015\n")
        pgasw10 = Responder("Press \[Enter\] to continue", "\n")

        pgasw11 = Responder("Port \[5432\]", "\n")
        pgasw12 = Responder("Please choose an option \[1\]", "766\n")

        watchers=[pgasw1, pgasw2, pgasw3, pgasw4, pgasw5, pgasw6, pgasw7, pgasw8, pgasw9,pgasw10, pgasw11, pgasw12]

        con.run("%s/postgresql-10.6-1-linux-x64.run" % tdir, pty=True, watchers=watchers)

        if pgdata == '':
            pgdata = '/opt/PostgreSQL/10/data'

        print("pgdata is : %s" % pgdata)
        self.cfg1(con, pgdata)
        if para["plpython"] != 'plpython34':
            version = para["plpython"]
            self.plpython(con, version)


    def cfg1(self,c, pgdata):
        c.run(f"""echo  'host all all all md5' >>{pgdata}/pg_hba.conf""" , pty=True)
        c.run("""systemctl restart postgresql-10""", pty=True)


    def plpython(self,c, version):
        dir = os.path.join(os.path.dirname(__file__), 'plpython', f'{version}.so' )
        print(dir)
        c.put(dir, '/opt/PostgreSQL/10/lib/postgresql/')
        c.run("rm -rf /opt/PostgreSQL/10/lib/postgresql/plpython3.so")
        c.run(f"mv /opt/PostgreSQL/10/lib/postgresql/{version}.so /opt/PostgreSQL/10/lib/postgresql/plpython3.so")
        c.run("chmod -R 755  /opt/PostgreSQL/10/lib/postgresql/plpython3.so")
        c.run("chown root:daemon  /opt/PostgreSQL/10/lib/postgresql/plpython3.so")


    def master_slave(self,conp1, conp2, master_data, slave_data):
        #主从

        c = Connection(conp2[0], connect_kwargs={"password": conp2[1]})
        c1 = Connection(conp1[0], connect_kwargs={"password": conp1[1]})
        c1.run(f"sed -i '/host replication all all md5/d' {master_data}/pg_hba.conf ", pty=True)
        c1.run(f"echo 'host replication all all md5' >>{master_data}/pg_hba.conf ", pty=True)
        c1.run("systemctl restart postgresql-10", pty=True)

        c.run("systemctl stop postgresql-10", pty=True)
        c.run("rm -rf %s" % slave_data, pty=True)
        mhost = conp1[0]
        master_host = mhost[mhost.index("@") + 1:mhost.index(":")]
        print(master_host)
        c.run("export PGPASSWORD='since2015' && /opt/PostgreSQL/10/bin/pg_basebackup -h %s -R -D %s -U postgres " % (master_host, slave_data), pty=True)
        c.run("chown -R postgres:root %s" % slave_data, pty=True)
        c.run("chmod 0700 %s" % slave_data, pty=True)
        c.run("systemctl restart postgresql-10", pty=True)

if __name__ == '__main__':
    pin = [
        ["root@172.16.16.4:22", "@jacky666", "seg3"],
        ["root@172.16.16.5:22", "@jacky666", "seg2"],
        ["root@172.16.16.6:22", "@jacky666", "seg1"]
    ]
    