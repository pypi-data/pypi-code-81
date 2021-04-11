from fabric import Connection
from invoke import Responder
import shutil
import os ,re
from lmfinstall import common
import sys ,time
from lmf.tool import down_file,mythread
import copy
import traceback 
import boto3
from io import BytesIO
from zljd.settings import gp_settings
class oss:
    def __init__(self,conp):
        self.conp=conp
        self.ak=gp_settings['jdyun']['ak']
        self.sk=gp_settings['jdyun']['sk']
        self.mount_dir="/jdoss"
        self.bucket='bst-oss1'
        self.endpoint="http://s3.cn-north-1.jdcloud-oss.com"
        self.endpoint_inter="http://s3-internal.cn-north-1.jdcloud-oss.com"
        if __name__=='__main__':
             path=os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),'data','s3fs-fuse-master.zip')
        else:

            path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','s3fs-fuse-master.zip')

        self.s3fs_file=path
        #"D:\\迁移部署\\s3fs-fuse-master.zip"
        self.internal=True
        #"echo 68B7C245223A75823C9F7AD47D20B12B:8CD17F4043787D4AF6F3A36174B9BAF0 > /root/.passwd-s3fs"%(self.ak,self.sk)
        #chmod 600 /root/.passwd-s3fs

    def get_gpbackup_yaml(self,folder):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        cfg="""executablepath: /usr/local/greenplum-db/bin/gpbackup_s3_plugin
               options: 
                  endpoint: %s
                  aws_access_key_id: %s
                  aws_secret_access_key: %s
                  bucket: %s
                  folder: %s
        """%(url,self.ak,self.sk,self.bucket,folder)
        cfg=cfg.split("\n")
        cfg=[w.strip() for w in cfg]
        cfg=cfg[0]+"\n"+"\n  ".join(cfg[1:])
        return cfg 


    def s3fs_pre(self):
        conp=self.conp
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        c.run("yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel unzip -y",pty=True)
        c.put(self.s3fs_file,'/root')
        c.run("unzip /root/s3fs-fuse-master.zip  && cd s3fs-fuse-master && ./autogen.sh &&  ./configure &&  make  &&  make  install",pty=True)




    def mount(self):
        conp=self.conp
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        tdir=self.mount_dir
        if c.run("test -f %s"%tdir,warn=True).failed:
            c.run("mkdir -p %s"%tdir)
        c.run("chmod -R 777 %s"%tdir)
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        c.run("echo %s:%s > /root/.passwd-s3fs"%(self.ak,self.sk),pty=True)
        c.run("chmod 600 /root/.passwd-s3fs",pty=True)
        cmd="""s3fs %s %s -o passwd_file=/root/.passwd-s3fs  -o url=%s    -o allow_other -o multipart_size=100  -o use_cache='/data/cache' -o del_cache  -o umask=000 """%(self.bucket,self.mount_dir,url)
        print(cmd)
        c.run(cmd,pty=True)

    def umount(self):
        conp=self.conp
        c=Connection(conp[0],connect_kwargs={"password":conp[1]})
        tdir=self.mount_dir
        c.run("umount  %s"%tdir,pty=True )
        c.run("rm -rf /root/.passwd-s3fs ",pty=True)

    def down_file(self,file_src,file_dst):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        s3 = boto3.client(  
            's3',  
            aws_access_key_id=self.ak,  
            aws_secret_access_key=self.sk,  
            #下面给出一个endpoint_url的例子  
            endpoint_url=url  
            ) 
        s3.download_file('bst-oss1',file_src,file_dst)

    def delete_file(self,filename):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        s3 = boto3.resource('s3',  
            aws_access_key_id=self.ak, 
            aws_secret_access_key=self.sk,  
            endpoint_url=url  )

        bucket = s3.Bucket(self.bucket)
        obj = bucket.Object(filename)
        obj.delete()


    def list_dir(self,dir):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        s3 = boto3.client(  
            's3',  
            aws_access_key_id=self.ak,  
            aws_secret_access_key=self.sk,  
            #下面给出一个endpoint_url的例子  
            endpoint_url=url  
            ) 
        a=s3.list_objects(Bucket=self.bucket,Prefix=dir)
        arr=[ w['Key'][len(dir):] for w in a['Contents']]
        arr=set( next(filter(lambda x:x!='',w.split('/')) ) for w in arr)
        if '' in arr:arr.remove('')
        return arr


    def upload_file(self,filename,tarname):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        s3 = boto3.client(  
            's3',  
            aws_access_key_id=self.ak,  
            aws_secret_access_key=self.sk,  
            #下面给出一个endpoint_url的例子  
            endpoint_url=url  
            ) 

        s3.upload_file(
            filename ,self.bucket, tarname,
            ExtraArgs={'ACL':'public-read'}
        )

class  web_oss(oss):
    def __init__(self,conp=None):
        super().__init__(conp=conp)
        self.bucket='bst-image'
        self.inits3()

    def  inits3(self):
        if self.internal:
            url=self.endpoint_inter
        else:
            url=self.endpoint
        self.s3 = boto3.client(  
            's3',  
            aws_access_key_id=self.ak,  
            aws_secret_access_key=self.sk,  
            #下面给出一个endpoint_url的例子  
            endpoint_url=url  
            ) 
    def upload_file(self,filename,tarname):
        self.s3.upload_file(
            filename ,self.bucket, tarname,
            ExtraArgs={'ACL':'public-read'}
        )
    def upload_file_byte(self,file_byte,tarname):
        f=BytesIO(file_byte)
        self.s3.upload_fileobj(f ,self.bucket, tarname,
            ExtraArgs={'ACL':'public-read'})

if __name__=='__main__':
    from lmf.dbv2 import db_query
    conp=["root@10.0.64.58:22","BST@web2020610","work7"]
    # conp=["root@10.0.64.4:22","BST@2020","work7"]
    m=oss(conp=conp)
    m.bucket='bst-image'
    # w=web_oss()
    
    m.mount()
    # w.umount()
