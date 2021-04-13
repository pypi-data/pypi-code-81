from sqlalchemy import create_engine
import multiprocessing 
import pandas as pd
from pandas import DataFrame
import datetime

class MigrateTable(object):

    '''
    class for Migrate Tables between different databases
    '''
    def __init__(self,configs):
        '''
            configs for create_engine in sqlalchemy, examples as below.
            configs = {
            'mysql': {'user':'thomas','pwd':'123456','address':'192.168.3.9:3306','database':'zftest','mydb':'mysql+pymysql'},
            'clickhouse':{'user':'default','pwd':'','address':'192.168.3.9:8123','database':'zftest','mydb':'clickhouse'}
            }
        '''
        self.configs = configs
    def connect(self,config):
        '''
        create engine for a particular database
        '''
        checks = ['user','pwd','address','database']
        for check in checks:
            if check not in config:
                raise Exception('config dont have {} info'.format(check))

        user = config.get('user')
        pwd = config.get('pwd')
        address = config.get('address')
        database = config.get('database')
        mydb = config.get('mydb') 
        db_uri = '{mydb}://{user}:{pwd}@{address}/{database}'.format(mydb=mydb,user=user,pwd=pwd,address=address,database=database)
        engine = create_engine(db_uri)
        return engine

    def _get_row_counts(self,db,table_name):
        engine = self.connect(configs[db])
        data = engine.execute("select count(1) from {}".format(table_name))
        res = data.fetchall()
        return res[0][0]

    def mysql_to_clickhouse_batch(self,table_from,table_to,batch_size=10000,pool = 4,convert_func=None):
        '''
        Migrate data from mysql to clickhouse in a parallel way

        table_from: table name in mysql
        table_to: table name in clickhouse
        batch_size: number of records in one batch
        pool: how many cores to use 
        convert_func: user-defined function for converting data type or adding new things during the migration

        '''
        row_counts = self._get_row_counts('mysql',table_from)
        tasks = [(self,table_to,table_from,i,batch_size,convert_func) for i in range(0,row_counts,batch_size)]
        with multiprocessing.Pool(pool) as pool:
            res = pool.starmap_async(MigrateTable._mysql_to_clickhouse, tasks) 
            res = res.get()
        return res 

    def _mysql_to_clickhouse(self,table_to,table_from,start,size,convert_func=None):
        try:
#            print('processing {} to {}'.format(start,start+size-1))
            engine = self.connect(configs['mysql'])
            data = engine.execute("select * from {} limit {},{}".format(table_from,start,size))
            df = DataFrame(data.fetchall(),columns = data.keys())
            # sqlalchemy-clickhouse did not load the last one record, so we need to add one records for it.
            df.loc[df.shape[0]] = df.loc[0]
            if convert_func is not None:
                convert_func(df)
            else:
                df = df.applymap(lambda x: str(x) if pd.notnull(x) else None)
            engine = self.connect(configs['clickhouse'])
            df.to_sql(table_to,engine,if_exists = 'append',index=False)
#            print('finished {} to {}'.format(start,start+size-1))
            return True,'{} to {} success'.format(start,start+size-1)
        except Exception as e:
            return False,'{} to {} failed: ' + str(e)


if __name__ == '__main__':
    configs = {
            'mysql': {'user':'thomas','pwd':'123456','address':'192.168.3.9:3306','database':'zftest','mydb':'mysql+pymysql'},
            'clickhouse':{'user':'default','pwd':'','address':'192.168.3.9:8123','database':'zftest','mydb':'clickhouse'}
            }
    mt = MigrateTable(configs)

    def sample_convert_func(df):
        columns = ['TradeDate','Open','High','Low','Close','TS']
        for col in columns:
            df[col] = df[col].apply(lambda x: str(x) if pd.notnull(x) else None)
        df['Status'] = 1

    res = mt.mysql_to_clickhouse_batch('HistPrice','HistPrice_all',batch_size=500,convert_func=sample_convert_func)
    print(res)
