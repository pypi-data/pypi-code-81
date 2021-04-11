
#从Python SDK导入BCC配置管理模块以及安全认证模块  pip install bce-python-sdk  解压 python setup.py install 
## 加密模块部分出问题，安装包的时刻解压后修改setup.py
import baidubce 
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
#导入BCC相关模块 
from baidubce.services.bcc import bcc_client 
from baidubce.services.bcc import bcc_model 
from baidubce.services.bcc.bcc_model import EphemeralDisk
import time 

class sdk:
    def __init__(self):

        self.ak="cdccee1dc9a1451f9bd0a9b6a3ded2c5"
        self.sk="de2ff91b959d48869618872273ed083a"
        config = BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk),endpoint='http://bcc.gz.baidubce.com')
        self.client = bcc_client.BccClient(config)

        self.app_init()

    def app_init(self):
        self.base=[
        ('172.16.0.10','i-HDvZqU9m','Since2015!'),
        ('172.16.0.11','i-VRzEEH3I','Since2015!'),
        ('172.16.0.12','i-B87IL1Ce','Since2015!'),
        ('172.16.32.6','i-yaUOeAT8','Since2015!'),
        ]

    def query(self,instance): 

        result=self.client.get_instance(instance)
        return result

    def start(self,instance): 
        try:
            result=self.client.start_instance(instance)
            print(result)
        except Exception as e:
            print(e)

    def stop(self,instance): 

        try:
            result=self.client.stop_instance(instance)
            print(result)
        except Exception as e:
            print(e)

    def restart(self,instance): 

        try:
            result=self.client.reboot_instance(instance)
            print(result)
        except Exception as e:
            print(e)
    def rebuild(self,instance,password,image_id='m-ZndjGpKK'):

        self.client.rebuild_instance(instance,image_id=image_id,admin_pass=password)

    def list_images(self,tag='System'):

        result=self.client.list_images(image_type=tag,max_keys=100)
        return result 

    def modifypassword(self,instance,password):
        result=self.client.modify_instance_password(instance,password)
        return result

    def check(self,hosts,status):
        #"stopped,running,rebuilding"
        for w in hosts:
            result=self.query(w[1])
            result=result.instance.status
            if result!=status:
                print(w[0],result)
                return False
        return True

    def get_hosts_status(self,hosts):
        #"stopped,running,rebuilding"
        for w in hosts:
            result=self.query(w[1])
            result=result.instance.status
            print(w[0],result)

    def rebuild_hosts(self,h_type,myhosts=None):
        if h_type=='myhosts':
            hosts=myhosts
        elif h_type=='base':
            hosts=self.base
        # for w in hosts:
        #     print(w[0])
        #     print("stopping--%s"%w[0])
        #     self.stop(w[1])
        # while not self.check(hosts,'Stopped'):
        #     time.sleep(10)

        for w in hosts:
            print("rebuilding--%s"%w[0])
            self.rebuild(w[1],w[2])


        while not self.check(hosts,'Running'):
            time.sleep(10)

        #修改密码
        # for w in hosts:
        #     print("modifypassword--%s"%w[0])
        #     self.modifypassword(w[1],w[2])
        # while not self.check(hosts,'Running'):
        #     time.sleep(5)

    def fq1(self):
        self.rebuild_hosts('base')
