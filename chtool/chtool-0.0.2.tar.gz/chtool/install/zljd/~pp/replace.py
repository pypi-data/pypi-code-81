from zljd.core.sdk import sdk 
from zljd.app.jd_web_test import jd_web_test_exam 
from zljd.app.jd_web_oss import jd_web_exam 
from zljd.backup.restore import restore 
import time
#替换环境
##web  app1   app5 

#测试环境，替换web部分3台服务器及其代码
def web_test_replace():
    sdk().rebuild_hosts('web_test')
    m=jd_web_test_exam(True)
    m.web_file_date='20200801'
    m.web_prt()


#测试环境，替换app1s数据库
def app1_test_replace():
    m=jd_web_test_exam(True)
    
    m.data_file_date=['20200808','20200808','20200808']
    m.gg_html=False
    m.refresh_para()

    m.db_app1_prt3()
    m.db_app1_prt5()
    pass

def web_replace():
    bg=time.time()
    sdk().rebuild_hosts('web')
    m=jd_web_exam(True)
    m.web_file_date='20200811'
    m.web_prt()
    ed=time.time()
    cost=int(ed-bg)
    print("totally cost %d s "%cost)


def app1_replace():
    bg=time.time()
    m=jd_web_exam(True)
    
    m.data_file_date=['20200811','20200811','20200811']
    m.gg_html=False
    m.refresh_para()

    m.db_app1_prt3()
    m.db_app1_prt5()
    ed=time.time()
    cost=int(ed-bg)
    print("totally cost %d s "%cost)
if __name__=='__main__':
    # web_replace app1_replace 
    #web_replace()#1051
    #web_replace()
    app1_replace()  #1330
    
    #app1_test_replace()

    pass

    # env GPSESSID=0000000000 GPERA=0636064da30bbb37_200805003530 $GPHOME/bin/pg_ctl -D /data/greenplum/data/datap2/seg28 -l /data/greenplum/data/datap2/seg28/pg_log/startup.log -w -t 600 -o " -p 40002 " start 2>&1

    # env GPSESSID=0000000000 GPERA=0636064da30bbb37_200805003530 /usr/local/greenplum-db/bin/pg_ctl  -D /data/greenplum/data/datap2/seg28 -l /data/greenplum/data/datap2/seg28/pg_log/startup.log -w -t 600 -o " -p 40002 " start 2>&1