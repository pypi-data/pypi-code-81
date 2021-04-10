from zljd.backup.restore import restore 
from zljd.backup.dump import dump 
from lmf.tool import mythread
import time 
class jd_db4_data:
    def __init__(self):
        self.db1_dbs=['anhui', 'beijing', 'chongqing', 'fujian', 'gansu', 
        'guangdong', 'guangxi', 'guizhou', 'hainan', 'hebei', 'heilongjiang']

        self.db2_dbs=['credit','henan', 'hubei', 'hunan', 'jiangsu', 'jiangxi', 'jilin', 'liaoning','mohurd']

        self.db3_dbs=['neimenggu', 'ningxia', 'qinghai', 'shandong', 'shanghai', 'shanxi', 
        'shanxi1', 'sichuan', 'swf', 'tianjin', 'wenshu', 'wx', 'xinjiang', 'xizang', 'yunnan', 'zhejiang']

        self.db4_dbs=['daili', 'jianshetong', 'personlock', 'qg', 'qycg', 'wxggzy', 'xingou', 'yszz'
        , 'zljzsheng', 'zlmine', 'zlqy', 'zlshenpi', 'zlsys']

        self.db_map={"db1":self.db1_dbs,"db2":self.db2_dbs,"db3":self.db3_dbs,"db4":self.db4_dbs}
    def add_data(self,loc,dmpdate):
        bg=time.time()
        def f1(app):
            self.add_data_db(loc=loc,dmpdate=dmpdate,app=app)
        apps=list(self.db_map.keys())
        mythread(f=f1,arr=apps).run(len(apps))
        ed=time.time()
        cost=int(ed-bg)
        print("totally-cost-%d s"%cost)
        
    def add_data_db(self,loc,dmpdate,app='db1'):
        m=restore(loc=loc,app=app)
        for db in self.db_map[app]:
            m.db(db,dmpdate)

    def dump_data(self,loc):
        bg=time.time()
        def f1(app):
            self.dump_data_db(loc=loc,app=app)
        apps=list(self.db_map.keys())
        mythread(f=f1,arr=apps).run(len(apps))
        ed=time.time()
        cost=int(ed-bg)
        print("totally  ---cost %d s"%cost)
    def dump_data_db(self,loc,app='db1'):
        m=dump(loc=loc,app=app)
        for db in self.db_map[app]:
            m.db(db)


if __name__=="__main__":
    dbs=['personlock',  'qg' ,'qycg','zlqy','zlshenpi','zlsys' ]#,  'postgres'
    m=restore(loc='jdyun',app='db4')
    for db in dbs:
            m.db("%s"%db,'20200811')
    #jd_db4_data().add_data_db(loc='jdyun',dmpdate="20200811",app='db3')
    #jd_db4_data().add_data(loc='jdyun',dmpdate="20200630")
    pass
