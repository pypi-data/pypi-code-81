from zljd.backup.restore import restore 
from zljd.backup.dump import dump 
import time 
class jd_web_data:
    def __init__(self):
        self.app5_dbs=['biaost']
        self.app1_tbs=['public.gg_html']
        
    def add_data(self,loc,dmpdate):
        bg=time.time()
        m=restore(loc=loc,app='app5')
        for db in self.dbs:
            m.db(db,dmpdate)

        m=restore(loc=loc,app='app1')
        for tb in self.app1_tbs:

            m.tb(tb,dmpdate)
        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)

    def dump_data(self,loc):
        bg=time.time()
        m=dump(loc=loc,app='app5')
        for db in self.app5_dbs:
            m.db(db)
        m=dump(loc=loc,app='app1')
        for tb in self.app1_tbs:
            m.tb(tb)
        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)

if __name__=='__main__':
    #jd_web_data().dump_data(loc='jdyun')
    pass