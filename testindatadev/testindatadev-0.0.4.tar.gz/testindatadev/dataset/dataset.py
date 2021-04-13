import sys
import os

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from s3.minio.minio import YcMinio
from dataset.request import Request

# 约定：dataset下的所有方法均是对数据集的操作，非clint调用的地方，严禁出现bucket之类的存储对象用语
# 本类用来屏蔽各种存储对象(oss, minio, 七牛)之间的差异，通过type构造不同的客户端解决问题，类似工厂类
# 各个OSS均需要实现本类中的所有方法
# bucket = dataset
# object = record
class Dataset():
    def __init__(self, T_key, datasetName, ip):
        self.req = Request(T_key, datasetName, ip)
        info = self.req.GetAccess()
        self.access_key = info['access_key']
        self.secret_key = info['secret_key']
        self.endpoint = info['endpoint']
        self.bucket = info['bucket']
        self.type = info['type']
        self.datasetName = datasetName
        self.ip = ip
        if self.type == "minio":
            self.client = YcMinio(self.access_key, self.secret_key, self.endpoint)
            if datasetName not in self.ListAllDataset():
                raise Exception("can not connect to the dataset, please make sure you have the correct access rights and the dataset exists!")
        else:
            raise Exception("尚未支持其他类型的云存储")


    #列出所有数据集
    def ListAllDataset(self, datasetName="", recu=False):
        ret = [dataset.replace("/", "") for dataset in self.client.ListObjects(self.bucket)]
        return ret

    #列出谋个数据集的所有文件
    def ListAllFile(self):
        ret = [file for file in self.client.ListObjects(self.bucket, prefix=self.datasetName, recursive=True)]
        return ret

    #直传文件
    def PutFilesToDataset(self, datasetName, rootPath, ext="", batchNum=0):
        total = 0        
        i = 0
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    total += 1

        dirname = os.path.dirname(rootPath.rstrip("/"))
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    filePath = os.path.join(root, fileName)
                    objectName = filePath.replace(dirname, "")
                    self.PutFileToDataset(self.bucket, datasetName + objectName, filePath)
                    i += 1
                    per = (i * 100) // total
                    showText = filePath + " =====> " + datasetName + objectName
                    process = "\r[%3s%%]: %s" % (per, showText)
                    print(process)

        print("success total:" + str(total))
        return True
    
    def PutFileToDataset(self, objectName, filePath):
        self.client.PutObject(self.bucket, self.datasetName + "/" + objectName, filePath)

    def DeleteFromDataset(self, objectName):
        self.client.DeleteObject(self.bucket, self.datasetName + "/" + objectName)
        return True

    def SyncDataToWeb(self, data):
        info = self.req.Upload(data)
        return info

    def Delete(self, referId):
        info = self.req.Delete(referId)
        #todo 删除oss文件
        # self.DeleteFromDataset(self.datasetName, info["osspath"])
        return info

    def GetData(self, offset, limit):
        info = self.req.GetData(offset, limit)
        for item in info["items"]:
            item['accessUrl'] = self.client.PresignedGetObject(self.bucket, item["path"], expire=7)

        return info



