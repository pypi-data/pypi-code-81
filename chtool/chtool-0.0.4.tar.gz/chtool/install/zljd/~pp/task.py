from zljd.app.jd_gp import jd_gp_exam
from zljd.app.jd_gp_ext import jd_gp_ext
from zljd.core.sdk import sdk 
from zlgp3.dm2.usage import usage
from zljd.backup.restore import restore 
from zlgp3.dm2.for_app5 import app5 
class test_env:
    def __init__(self):
        self.pin=[
                    ['root@10.30.16.27:22','BST@dwtest20200729','metadb1'],
                    ['root@10.30.16.28:22','BST@dwtest20200729','metadb2'],
                    ['root@10.30.16.29:22','BST@dwtest20200729','master1'],
                    ['root@10.30.16.30:22','BST@dwtest20200729','master2'],
                    ['root@10.30.16.31:22','BST@dwtest20200729','master3'],
                    ['root@10.30.16.32:22','BST@dwtest20200729','master4'],
                    ['root@10.30.16.33:22','BST@dwtest20200729','datanode1'],
                    ['root@10.30.16.34:22','BST@dwtest20200729','datanode2'],
                    ['root@10.30.16.35:22','BST@dwtest20200729','datanode3'],
                    ['root@10.30.16.36:22','BST@dwtest20200729','datanode4'],
                    ['root@10.30.16.37:22','BST@dwtest20200729','datanode5'],
                    ['root@10.30.16.38:22','BST@dwtest20200729','datanode6'],
                    ['root@10.30.16.39:22','BST@dwtest20200729','datanode7'],
                    ['root@10.30.16.40:22','BST@dwtest20200729','datanode8'],
                    ['root@10.30.16.41:22','BST@dwtest20200729','datanode9'],
                    ['root@10.30.16.42:22','BST@dwtest20200729','datanode10'],
                    ['root@10.30.16.43:22','BST@dwtest20200729','datanode11'],
                    ['root@10.30.16.44:22','BST@dwtest20200729','datanode12'],
                    ['root@10.30.16.45:22','BST@dwtest20200729','datanode13'],
                    ['root@10.30.16.46:22','BST@dwtest20200729','datanode14'],
                    ['root@10.30.16.47:22','BST@dwtest20200729','datanode15'],
                    ]


    def task1_test(self):
        ##提供基础GP环境
        sdk().rebuild_hosts('gp_dw_test')
        m=jd_gp_exam(True)
        m.pin=self.pin
        m.hdp_pin=m.get_pin(range(2,21))

        m.gp_pin=m.get_pin([4,*range(6,21),5])

        m.pg_master,m.pg_slave=m.get_pin([0,1])
        ip=m.pg_master[0]
        ip=ip[ip.index("@")+1:ip.index(":")]

        m.db_conp=['postgres','since2015',ip,'ambari','public']
        m.gp_oss_date='20200630'

        m.oss_internal=True
        m.local_file_dir="D:\\jingdong_gpsystest_download"
        m.init_local_file()
        m.init_oss_file()

        m.gp_data_files=[]

        m.task()


    def task2_test(self):
        m=jd_gp_ext()

        m.pin=self.pin
        
        m.fstype="jdoss"
        m.gp_pin=m.pin[4:]
        ip=m.gp_pin[0][0]
        ip=ip[ip.index('@')+1:ip.index(':')]
        m.gp_master=['gpadmin','since2015',ip,'base_db','public']

        m.local_file_dir="D:\\jingdong_gpexttest_download"
        m.oss_internal=True
        m.docker_file="docker_ljt_20200605.tar"
        m.gpbackup_file="pivotal_greenplum_backup_restore-1.17.0-1-gp6-rhel-x86_64.gppkg"
        m.dmpdate='20200801'
        m.loc='jdyun_test'
        m.env()


    def task3_test(self):
        loc='jdyun_test'
        usage(loc=loc).from_zero()
        app5(loc=loc).pre()
        usage(loc=loc).run_all(f='add_quyu_without',num=6)



class env:
    def __init__(slef):

        pass 

    def task1(self):
        
        sdk().rebuild_hosts('gp_dw')
        m=jd_gp_exam(True)
        m.task()

    def task2(self):
        m=jd_gp_ext()
        m.dmpdate='20200823'
        m.env()

    def task3(self):
        loc='jdyun'
        usage(loc=loc).from_zero()
        app5(loc=loc).pre()
        usage(loc=loc).run_all(f='add_quyu_without',num=6)

if __name__=="__main__":
    m=env()
    # m.task1()
    # m.task2()
    m.task3()