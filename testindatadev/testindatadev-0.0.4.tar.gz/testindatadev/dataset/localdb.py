import sys, os
import sqlite3

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from utils import util
from file import File

class LocalDb():
    def __init__(self, commitId=""):
        self.commitId = commitId

        self.newDbFlag = False
        if self.commitId  == "":#新db
            self.commitId = util.getRandomSet(32)
            self.newDbFlag = True



        home = "USERPROFILE" if os.name == "nt" else "HOME"
        configDir = os.path.join(os.environ[home], ".tda/")
        if not os.path.exists(configDir):
            os.makedirs(configDir)

        self.dbDir = os.path.join(configDir, self.commitId)
        if not os.path.exists(self.dbDir):
            os.makedirs(self.dbDir)

        self.dbFile = os.path.join(self.dbDir, self.commitId + ".db")
        if not os.path.exists(self.dbFile) and not self.newDbFlag:
            raise Exception(f"commit db [{self.commitId}] not exist, have you ever commited them?")

        if not os.path.exists(self.dbFile) and self.newDbFlag:
            self.initDb()

    def initDb(self):
        self.conn = sqlite3.connect(self.dbFile)
        self.cur = self.conn.cursor()

        if self.newDbFlag:
            createSql = '''CREATE TABLE TDADATA
                   (filepath CHAR(1024) PRIMARY KEY NOT NULL,
                    osspath CHAR(1024) NOT NULL,
                    objectPath CHAR(1024) NOT NULL,
                    filename CHAR(521) NOT NULL,
                    md5 CHAR(32) NOT NULL,
                    referid CHAR(128) NOT NULL,
                    filesize INT NOT NULL,
                    metadata CHAR(1024) NOT NULL,
                    labeldata BLOB NOT NULL
                   );'''
            self.cur.execute(createSql)

        self.conn.close()

    def close(self):
        self.conn.close()

    def getDataByFilepath(self, filepath):
        self.conn = sqlite3.connect(self.dbFile)
        self.cur = self.conn.cursor()
        sql = f"SELECT * FROM TDADATA WHERE filepath = '{filepath}';"
        res = self.cur.execute(sql)
        return res


    def insertVal(self, data = []):
        self.conn = sqlite3.connect(self.dbFile)
        self.cur = self.conn.cursor()

        for file in data:
            file.SelfCheck()
            sql = f"SELECT * FROM TDADATA WHERE filepath = '{file.filepath}';"
            self.cur.execute(sql)
            res = self.cur.fetchone()
            if res != None:
                print(file.filepath + " already commited, continue! you can updload them whenever you want.")
                continue

            sql = f"INSERT INTO TDADATA (filepath, osspath, objectPath, filename, md5, referid, filesize, metadata, labeldata) VALUES ('{file.filepath}', '{file.osspath}', '{file.objectPath}', '{file.filename}', '{file.md5}', '{file.referId}', '{file.filesize}', '{file.metadata.ToString()}', '{file.labeldata.ToString()}')"

            self.cur.execute(sql)

        self.conn.commit()
        self.conn.close()


    def fetchAll(self):
        ret = []
        self.conn = sqlite3.connect(self.dbFile)
        self.cur = self.conn.cursor()
        sql = f"SELECT * FROM TDADATA;"
        res = self.cur.execute(sql)
        for row in res:
            # tmpFile = File()
            # tmpFile.filepath = row[0]
            # tmpFile.osspath = row[1]
            # tmpFile.filename = row[2]
            # tmpFile.md5 = row[3]
            # tmpFile.referid = row[4]
            # tmpFile.filesize = row[5]
            # tmpFile.metadata = row[6]
            # tmpFile.labeldata = row[7]

            tmp = {
                "filepath":row[0],
                "osspath":row[1],
                "objectPath":row[2],
                "filename":row[3],
                "md5":row[4],
                "referid":row[5],
                "filesize":row[6],
                "metadata":row[7],
                "labeldata":row[8],
            }

            ret.append(tmp)
        self.conn.close()
        return ret






