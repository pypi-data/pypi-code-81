import os
import sys
import json
import re

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from dataset.dataset import Dataset
from dataset.file import File
from utils import util
from dataset.localdb import LocalDb

#sdk入口
class TDA():
    def __init__(self, T_key):
        self.T_key = T_key
        self.commitFlag = False
        self.commitId = ""
        self.datasetName = ""
        self.fileList = []


    def SetDataset(self, datasetName, ip=""):
        if ip:
            trueIp = re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', ip)
            self.ip = trueIp.group()

        self.datasetName = datasetName
        self.dataset = Dataset(self.T_key, datasetName, self.ip)

    def RiseException(self):
        raise Exception("You have not set the dataset name yet!")


    def ListAllFile(self, recu=False):
        if not self.datasetName:
            self.RiseException()

        return self.dataset.ListAllFile()


    def UploadFilesToDataset(self, rootPath, basepath="", ext="", batchNum=0):
        if not self.datasetName:
            self.RiseException()

        syncData = []
        j = 0
        i = 0
        retInfo = {'succ': 0, 'fail': 0}
        dirname = os.path.dirname(rootPath.rstrip("/"))
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    filePath = os.path.join(root, fileName)
                    objectName = filePath.replace(dirname, "").lstrip("/")

                    if not basepath:
                        objectPath = objectName
                    else:
                        basepath = basepath.rstrip("/")
                        if filePath.find(basepath) < 0:
                            raise Exception(f"basepath must be part of filepath!")
                        objectPath = filePath.split(basepath + "/")[1]

                    self.__UploadFileToDataset(filePath, objectPath)
                    tmp = {
                        "ref_id": "",
                        "name": fileName,
                        "path": self.datasetName + "/" + objectPath,
                        "size": int(util.getFileSize(filePath)),
                        "md5": util.getFileMd5(filePath),
                        "meta": {},
                        "anotations": {},
                    }
                    syncData.append(tmp)
                    i += 1
                    j += 1

                    if j >= 1000:
                        j = 0
                        info = self.dataset.SyncDataToWeb(syncData)
                        retInfo["succ"] += info["succ"]
                        retInfo["fail"] += info["fail"]
                        syncData = []

        if len(syncData) >= 0:#最后几个没同步的数据
            info = self.dataset.SyncDataToWeb(syncData)
            retInfo["succ"] += info["succ"]
            retInfo["fail"] += info["fail"]

        return retInfo


    def UploadFileToDataset(self, filePath, basePath=""):
        basePath = basePath.rstrip("/")
        objectName = filePath.split(basePath)[1].lstrip("/")
        self.__UploadFileToDataset(filePath, objectName)
        syncData = {
            "ref_id": "",
            "name": os.path.basename(filePath),
            "path": self.datasetName + "/" + objectName,
            "size": int(util.getFileSize(filePath)),
            "md5": util.getFileMd5(filePath),
            "meta": {},
            "anotations": {},
        }

        info = self.dataset.SyncDataToWeb([syncData])

        return info


    def __UploadFileToDataset(self, filePath, objectName):
        if not self.datasetName:
            self.RiseException()
        return self.dataset.PutFileToDataset(objectName, filePath)

    def DeleteFileFromDataset(self, objectName):
        if not self.datasetName:
            self.RiseException()

        return self.dataset.DeleteFromDataset(objectName)

    def AddFile(self, filepath, basepath=""):
        if not self.datasetName:
            self.RiseException()

        file = File(filepath, basepath, self.datasetName)
        self.fileList.append(file)
        return file


    def Commit(self, commitId = ""):
        if not self.datasetName:
            self.RiseException()

        db = LocalDb(commitId)
        db.insertVal(self.fileList)
        db.close()

        self.commitFlag = True
        self.commitId = db.commitId
        return db.commitId


    def Upload(self, commitId = ""):
        if not self.datasetName:
            self.RiseException()

        if commitId != "":
            self.commitFlag = True
            self.commitId = commitId

        if not self.commitFlag:
            self.commitId = self.Commit(commitId)

        if not self.commitId:
            self.commitId = self.Commit(commitId)

        db = LocalDb(commitId)
        allData = db.fetchAll()

        syncData = []
        i = 0
        retInfo = {'succ': 0, 'fail': 0}
        for data in allData:
            self.__UploadFileToDataset(data["filepath"], data["objectPath"])
            tmp = {
                "ref_id":data["referid"],
                "name":data["filename"],
                "path":data["osspath"],
                "size":data["filesize"],
                "md5":data["md5"],
                "meta":json.loads(data["metadata"]),
                "anotations":json.loads(data["labeldata"]),
            }
            syncData.append(tmp)
            i += 1
            if i >= 1000:
                i = 0
                info = self.dataset.SyncDataToWeb(syncData)
                retInfo["succ"] += info["succ"]
                retInfo["fail"] += info["fail"]
                syncData = []


        if len(syncData) >= 0:#最后几个没同步的数据
            info = self.dataset.SyncDataToWeb(syncData)
            retInfo["succ"] += info["succ"]
            retInfo["fail"] += info["fail"]

        return retInfo

    def Delete(self, referId):
        if not referId:
            raise Exception("referId can not be empty")
        return self.dataset.Delete(referId)

    def GetData(self, offset=0, limit=100):
        if limit > 1000:
            raise Exception("limit must less than 1000")

        return self.dataset.GetData(offset, limit)









