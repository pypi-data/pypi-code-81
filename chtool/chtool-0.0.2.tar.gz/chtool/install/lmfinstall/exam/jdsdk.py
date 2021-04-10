from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.services.vm.client.VmClient import VmClient
from jdcloud_sdk.services.vm.apis.DescribeInstanceTypesRequest import DescribeInstanceTypesParameters, DescribeInstanceTypesRequest
from jdcloud_sdk.services.vm.apis.DescribeInstanceRequest  import  DescribeInstanceParameters,DescribeInstanceRequest
from jdcloud_sdk.services.vm.apis.StopInstanceRequest  import  StopInstanceParameters,StopInstanceRequest
from jdcloud_sdk.services.vm.apis.StartInstanceRequest  import  StartInstanceParameters,StartInstanceRequest
from jdcloud_sdk.services.vm.apis.RebuildInstanceRequest   import  RebuildInstanceParameters,RebuildInstanceRequest

from jdcloud_sdk.services.vm.apis.ModifyInstancePasswordRequest   import  ModifyInstancePasswordParameters,ModifyInstancePasswordRequest

import time 
import logging

class sdk:
    def __init__(self):
        self.access_key = '68B7C245223A75823C9F7AD47D20B12B'
        self.secret_key = '8CD17F4043787D4AF6F3A36174B9BAF0'
        self.credential = Credential(self.access_key, self.secret_key)
        logger = logging.getLogger('jd')
        self.client = VmClient(self.credential,logger=logger)
        self.region='cn-north-1'
        self.app_init()

    def modifypassword(self,instance,password,region=None):
        try:
            if region is None:
                parameters = ModifyInstancePasswordParameters(self.region,instance,password)
            else:
                parameters = ModifyInstancePasswordParameters(region,instance,password)
            request = ModifyInstancePasswordRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
            return resp.result
        except Exception as e:
            print(e)

    def query(self,instance,region=None):
        time.sleep(2)
        for i in range(5):
            try:
                if region is None:
                    parameters = DescribeInstanceParameters(self.region,instance)
                else:
                    parameters = DescribeInstanceParameters(region,instance)
                request = DescribeInstanceRequest(parameters)
                resp = self.client.send(request)
                if resp.error is not None:
                    print(resp.error.code, resp.error.message)
                if resp.result is None:continue
                print("jieguo------",resp.result['instance']['privateIpAddress'],resp.result['instance']['status'])
                return resp.result
            except Exception as e:

                print(e)

    def stop(self,instance,region=None):
        try:
            if region is None:
                parameters = StopInstanceParameters(self.region,instance)
            else:
                parameters = StopInstanceParameters(region,instance)
            request = StopInstanceRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
            return resp.result
        except Exception as e:
            print(e)

    def start(self,instance,region=None):
        try:
            if region is None:
                parameters = StartInstanceParameters(self.region,instance)
            else:
                parameters = StartInstanceParameters(region,instance)
            request = StartInstanceRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
            return resp.result
        except Exception as e:
            print(e)
    def rebuild(self,instance,password,region=None):
        try:
            if region is None:
                parameters = RebuildInstanceParameters(self.region,instance,password)
            else:
                parameters = RebuildInstanceParameters(region,instance,password)
            request = RebuildInstanceRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
            return resp.result
        except Exception as e:
            print(e)

    def check(self,hosts,status):
        #"stopped,running,rebuilding"
        for w in hosts:
            try:
                result=self.query(w[1])
                result=result['instance']['status']
                if result!=status:
                    print(w[0],result)
                    return False
            except:
                result=self.query(w[1])
                result=result['instance']['status']
                if result!=status:
                    print(w[0],result)
                    return False
        return True
    def get_hosts_status(self,hosts):
        #"stopped,running,rebuilding"
        for w in hosts:
            try:
                result=self.query(w[1])
                result=result['instance']['status']
                print(w[0],result)
            except:
                print(w)

    def exam(self):
        try:
            parameters = DescribeInstanceTypesParameters('cn-north-1')
            request = DescribeInstanceTypesRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
            return resp.result
        except Exception as e:
            print(e)
            # 错误处理

    def app_init(self):
        self.gp_dw=[
        ("10.0.64.26","i-trr59gof97","BST@2020610"),
        ("10.0.64.27","i-tfyvns7g18","BST@2020610"),

        ("10.0.64.28","i-tdxfy9y3aj","BST@2020610"),
        ("10.0.64.29","i-qhrnswt9qt","BST@2020610"),
        ("10.0.64.30","i-a0wy47az35","BST@2020610"),
        ("10.0.64.31","i-gcfov38316","BST@2020610"),

        ("10.0.64.32","i-o43oa0b99q","BST@2020610"),
        ("10.0.64.33","i-lobh7jueht","BST@2020610"),
        ("10.0.64.34","i-5ts4cx083m","BST@2020610"),
        ("10.0.64.35","i-pub6tk4d03","BST@2020610"),
        ("10.0.64.36","i-7qg6kodql1","BST@2020610"),
        ("10.0.64.37","i-iwny1mueuj","BST@2020610"),
        ("10.0.64.38","i-drc63vt35d","BST@2020610"),
        ("10.0.64.39","i-kc8wf9t06t","BST@2020610"),
        ("10.0.64.40","i-6a85gfp5s5","BST@2020610"),
        ("10.0.64.41","i-r2plu0an7d","BST@2020610"),
        ("10.0.64.42","i-26zmxlt9uq","BST@2020610"),
        ("10.0.64.43","i-2cxtcram20","BST@2020610"),
        ("10.0.64.44","i-t9tnl8drol","BST@2020610"),
        ("10.0.64.45","i-cfmxecd34y","BST@2020610"),
        ("10.0.64.46","i-jreqpt14ph","BST@2020610"),
        ]

        self.app5_1=[
        ("10.0.64.51","i-o3x1trj7qn","BST@2020610"),
        ("10.0.64.52","i-oup4t0fnno","BST@2020610"),
        ("10.0.64.53","i-v7plt1u0tz","BST@2020610"),
        ("10.0.64.54","i-ogz5tja8f5","BST@2020610"),
        ("10.0.64.55","i-ow37oq9rhm","BST@2020610"),
        ("10.0.64.56","i-17s6yrdcb8","BST@2020610"),
        ]

        self.app5_2=[
        ("10.0.64.57","i-haylqkmlvs","BST@2020610"),
        ("10.0.64.58","i-9xax34gw2n","BST@2020610"),
        ("10.0.64.59","i-rsflfcncz2","BST@2020610"),
        ("10.0.64.60","i-5r9mniyvom","BST@2020610"),
        ("10.0.64.61","i-dwp3aei7x0","BST@2020610"),
        ("10.0.64.11","i-1zkzmpv8is","BST@2020610"),
        ]

        self.pg_db=[
        ("10.0.64.21","i-uof4cdfkew","BST@2020610"),
        ("10.0.64.22","i-49c7xskok2","BST@2020610"),
        ("10.0.64.23","i-uz9adtca60","BST@2020610"),
        ("10.0.64.24","i-x40fqjqio0","BST@2020610"),
        ]


        self.airflow_1=[
        ("10.0.64.7","i-9xzw6c8wnj","BST@2020610"),
        ("10.0.64.8","i-vactgzc7p2","BST@2020610"),
        ("10.0.64.9","i-8b9a2duu7m","BST@2020610"),
        ("10.0.64.10","i-ns5d1z52sh","BST@2020610"),
        ]

        self.airflow_2=[
        ("10.0.64.50","i-y4d0cyz0yg","BST@2020610"),
        ("10.0.64.12","i-5rjyngg3ts","BST@2020610"),
        ("10.0.64.13","i-6v45i8jvt5","BST@2020610"),
        ("10.0.64.14","i-kenn4hb2qu","BST@2020610"),
        ("10.0.64.15","i-gjpxvlff1f","BST@2020610"),
        ("10.0.64.16","i-1yzm94i171","BST@2020610"),
        ("10.0.64.17","i-z30sxk8g3u","BST@2020610"),
        ("10.0.64.18","i-6h5uxcojrv","BST@2020610"),
        ("10.0.64.19","i-4be775jscy","BST@2020610"),
        ]

        self.win_1=[
        ("10.0.64.3","i-vvpi2pffpk","BST@2020610"),
        ("10.0.64.4","i-y8hb5bdtyt","BST@2020610"),
        ("10.0.64.5","i-53r482m6th","BST@2020610"),
        ("10.0.64.6","i-dustmpr4r4","BST@2020610"),
        ]

        self.win_2=[
        ("10.0.64.25","i-hj5w1ofxnb","BST@2020610"),
        ("10.0.64.20","i-cr5eg4zg7q","BST@2020610"),
        ]

        self.web=[
        ("10.0.64.47","i-y5s2nmun3o","BST@2020610"),
        ("10.0.64.48","i-xbqv5s6io1","BST@2020610"),
        ("10.0.64.49","i-ft12rv1abi","BST@2020610"),
        ]




    def rebuild_hosts(self,h_type,myhosts=None):
        if h_type=='gp_dw':
            hosts=self.gp_dw 
        elif h_type=='app5_1':
            hosts=self.app5_1
        elif h_type=='app5_2':
            hosts=self.app5_2
        elif h_type=='pg_db':
            hosts=self.pg_db
        elif h_type=='web':
            hosts=self.web
        elif h_type=='airflow_1':
            hosts=self.airflow_1
        elif h_type=='airflow_2':
            hosts=self.airflow_2
        elif h_type=='myhosts':
            hosts=myhosts
        elif h_type=='win_1':
            hosts=self.win_1
        elif h_type=='web':
            hosts=self.web


        for w in hosts:
            print(w[0])
            print("stopping--%s"%w[0])
            self.stop(w[1])
        while not self.check(hosts,'stopped'):
            time.sleep(10)

        for w in hosts:
            print("rebuilding--%s"%w[0])
            self.rebuild(w[1],w[2])

        while not self.check(hosts,'stopped'):
            time.sleep(10)
        for w in hosts:
            print("startting--%s"%w[0])
            self.start(w[1])
        while not self.check(hosts,'running'):
            time.sleep(10)

        #修改密码
        for w in hosts:
            print("modifypassword--%s"%w[0])
            self.modifypassword(w[1],w[2])

        self.restart_hosts(h_type,myhosts=myhosts)
            





    def restart_hosts(self,h_type,myhosts=None):
        if h_type=='gp_dw':
            hosts=self.gp_dw 
        elif h_type=='app5_1':
            hosts=self.app5_1
        elif h_type=='app5_2':
            hosts=self.app5_2
        elif h_type=='pg_db':
            hosts=self.pg_db
        elif h_type=='web':
            hosts=self.web
        elif h_type=='airflow_1':
            hosts=self.airflow_1
        elif h_type=='airflow_2':
            hosts=self.airflow_2
        elif h_type=='win_1':
            hosts=self.win_1
        elif h_type=='web':
            hosts=self.web
        elif h_type=='myhosts':
            hosts=myhosts

        for w in hosts:
            print(w[0])
            print("stopping--%s"%w[0])
            self.stop(w[1])
        while not self.check(hosts,'stopped'):
            time.sleep(10)


        for w in hosts:
            print("startting--%s"%w[0])
            self.start(w[1])
        while not self.check(hosts,'running'):
            time.sleep(10)

        self.get_hosts_status(hosts)
        print("，所有主机都已经重新启动")