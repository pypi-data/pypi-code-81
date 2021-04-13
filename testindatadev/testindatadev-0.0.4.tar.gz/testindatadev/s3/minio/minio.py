from minio import Minio
from minio.error import InvalidResponseError as ResponseError
from datetime import timedelta

#约定：s3包下面的所有文件均是对存储对象的操作，里面所有的变量，单词，描述，均是和存储对象相关的，不允许出现dataset相关的用语
class YcMinio():
    def __init__(self, access_key, secret_key, endpoint, secure=False):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint.replace("http://", "").replace("https://", "")
        self.secure = secure

        self.client = Minio(
            self.endpoint,
            access_key = self.access_key,
            secret_key = self.secret_key,
            secure = False
        )


    #创建bucket
    def CreateBucket(self, bucketName, location='cn-north-1'):
        try:
            self.client.make_bucket(bucketName, location)
        except ResponseError as err:
            raise Exception("create bucket failed", err)

    #列出所有的Dataset
    def ListAllBucket(self):
        ret = []
        buckets = self.client.list_buckets()
        for bucket in buckets:
            ret.append(bucket.name)

        return ret

    #列出某个Dataset下面的所有文件
    def ListObjects(self, bucketName, prefix=None, recursive=False):
        ret = []
        objects = self.client.list_objects(bucketName, prefix, recursive)
        for obj in objects:
            # ret.append(obj.objectName.encode('utf-8'))
            ret.append(obj.object_name)

        return ret

    #上传单个文件数据
    def PutObject(self, bucketName, objectName, file_path, content_type='application/octet-stream', metadata=None):
        try:
            self.client.fput_object(bucketName, objectName, file_path)
        except ResponseError as err:
            raise Exception("failed in putting file", err)

    #删除单个文件
    def DeleteObject(self, bucketName, objectName):
        try:
            self.client.remove_object(bucketName, objectName)
        except ResponseError as err:
            raise Exception("failed in deleting file", err)

    #获取访问地址
    def PresignedGetObject(self, bucketName, objectName, expire=7):
        try:
            return self.client.presigned_get_object(bucketName, objectName, expires=timedelta(days=expire))
        except ResponseError as err:
            raise Exception("failed in create presigned object url", err)
