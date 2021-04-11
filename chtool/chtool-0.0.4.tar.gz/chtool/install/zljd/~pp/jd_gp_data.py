from zljd.backup.restore import restore 
from zljd.backup.dump import dump 
import time 
class jd_gp_data:
    def __init__(self):
        # self.schemas=['bid','src','app']
        self.schemas=[]
        self.tbs=[
        # 'dm.qy_base','dm.qy_zhuce'
        # ,'dm.qy_zz','dm.qy_zcry'
        # ,'dm.qyzz','dm.qyzcry'
        # ,'dm.t_qyzcry'
        # ,'dm.t_qyzz'
        # ,
        'dm.t_qyzcry_result','dm.t_qyzz_result'
        ,"dm.dict_ry_zz"
        #,'dm.zlqy_t_qy_zhuce'
        ,'dm.t_person_pre',"dm.t_file_upload"
        ,'dm.feiyan','dm.dst_gg_meta','dm.algo_m_gg'] 

        self.tbs1=['dm.t_person','dm.t_zz']#,'dm.zlqy_t_qy_zhuce']#,'dm.t_file'
        
    def add_data(self,loc,dmpdate):
        bg=time.time()
        m=restore(loc=loc,app='gp')
        for schema in self.schemas:
            m.schema(schema,dmpdate)
        for tb in self.tbs:

            m.tb(tb,dmpdate)
        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)

    def dump_data(self,loc):
        #loc=aliyun 30300 s
        bg=time.time()
        m=dump(loc=loc,app='gp')
        for schema in self.schemas:
            m.schema(schema)
        for tb in self.tbs:
            m.tb(tb)

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)



    def add_data1(self,loc,dmpdate):
        bg=time.time()
        m=restore(loc=loc,app='gp')
        for schema in self.schemas:
            m.schema1(schema,dmpdate,leaf=True)
        for tb in self.tbs:

            m.tb1(tb,dmpdate,leaf=True)

        for tb in self.tbs1:

            m.tb(tb,dmpdate)
        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)


    def dump_data1(self,loc):
        #loc=aliyun 30300 s
        bg=time.time()
        m=dump(loc=loc,app='gp')
        for schema in self.schemas:
            print(schema)
            m.schema1(schema,leaf=True)
        for tb in self.tbs:
            print(tb)
            m.tb1(tb,leaf=True)
        for tb in self.tbs1:
            print(tb)
            m.tb(tb)

        ed=time.time()
        cost=int(ed-bg)
        print("totally cost --%d s "%cost)


if __name__=="__main__":
    #m=jd_gp_data()
    #algo_m_gg #7100s

    #m.dump_data1('jdyun')  #14150 #15000
    pass