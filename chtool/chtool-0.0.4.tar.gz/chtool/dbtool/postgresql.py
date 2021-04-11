import pandas as pd
from sqlalchemy import create_engine,types
from sqlalchemy.dialects.postgresql import TEXT
from io import StringIO
import datetime
import re
import psycopg2


class Transitory():
    def __init__(self,user,password,host,database,schema="public",table=False):
        self.database=database
        self.user=user
        self.password=password
        self.host=host.split(":")[0]
        self.port= "5432" if ':' not in self.host else self.host.split(":")[1]

        self.schema=schema
        self.table=table


    def db_command_ext(self,sql):
        conn = psycopg2.connect(database=self.database, user=self.user,port=self.port, password=self.password,host=self.host)
        # conn2.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()


    def db_query_engine(self,sql):
        con = create_engine("postgresql://%s:%s@%s/%s" % (self.user, self.password, self.host, self.database), encoding='utf-8')
        sql = "set search_path to %s;" % self.schema + sql

        df = pd.read_sql(sql, con)
        con.dispose()
        return df


    def db_query(self,sql):
        sql = "set search_path to %s;" % self.schema + sql

        conn = psycopg2.connect(database=self.database, user=self.user, port=self.port, password=self.password,
                                host=self.host)
        cur=conn.cursor()
        cur.execute(sql)
        conn.commit()

        result=cur.fetchall()
        conn.close()
        cur.close()

        return result


    def db_write(self,df, tb_name, datadict=None, if_exists='replace'):
        """
        conp[4] 影响表写入的schema

        tb_name 可写成 schema.tbname 形式， 也可写成 tbname 形式

        """

        tbname=tb_name.split('.')[-1]
        schema=tb_name.split('.')[0] if tb_name.find('.') else self.schema

        con = create_engine("postgresql://%s:%s@%s/%s" % (self.user, self.password, self.host, self.database), encoding='utf-8')

        def sqlcol(dfparam, text=None):

            dtypedict = {}
            for i, j in zip(dfparam.columns, dfparam.dtypes):

                if "object" in str(j):
                    if text == "postgresql-text":
                        dtypedict.update({i: TEXT()})
                    else:
                        try:
                            x = int(df[i].str.len().max() / 40) + 1
                        except:
                            x = 50
                        dtypedict.update({i: types.VARCHAR(length=x * 80)})

                if "datetime" in str(j):
                    dtypedict.update({i: types.DateTime()})

                if "float" in str(j):
                    dtypedict.update({i: types.Float(precision=3, asdecimal=True)})

                if "int" in str(j):
                    dtypedict.update({i: types.INT()})

            return dtypedict

        if datadict is None: datadict = sqlcol(df)
        if datadict == 'postgresql-text': datadict = sqlcol(df, 'postgresql-text')

        df.to_sql(tbname, con, if_exists=if_exists, index=False, schema=schema, dtype=datadict)
        con.dispose()

    def copy_from(self,dataf,table_name,columns):

        # dataframe类型转换为IO缓冲区中的str类型
        output = StringIO()
        dataf.to_csv(output, sep='!', index=False, header=False)

        output1 = output.getvalue()
        conn = psycopg2.connect(database=self.database, user=self.user, port=self.port, password=self.password,host=self.host)
        cur = conn.cursor()
        cur.copy_from(StringIO(output1), table_name,sep='!',columns=columns)
        conn.commit()
        cur.close()
        conn.close()

    def copy_from_shm(self,df, table_name, quyu, if_exists='replace'):
        import io
        import pandas as pd
        from sqlalchemy import create_engine
        arr = quyu.split('_')
        db, schema = arr[0], arr[1]
        db_engine = create_engine("postgresql://%s:%s@%s/%s" % (self.user, self.password, self.host, self.database), encoding='utf-8')
        string_data_io = io.StringIO()
        df.to_csv(string_data_io, sep='|', index=False)
        pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
        table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df, index=False, if_exists=if_exists, schema=schema)
        table.create()
        string_data_io.seek(0)
        string_data_io.readline()  # remove header
        with db_engine.connect() as connection:
            with connection.connection.cursor() as cursor:
                copy_cmd = "COPY %s.%s FROM STDIN HEADER DELIMITER '|' CSV" % (schema, table_name)
                cursor.copy_expert(copy_cmd, string_data_io)
            connection.connection.commit()

    def db_command(self,sql):

        con = psycopg2.connect(database=self.database, user=self.user, port=self.port,password=self.password,host=self.host)

        cur = con.cursor()
        cur.execute(sql)

        con.commit()
        cur.close()
        con.close()


class Persistent():
    def __init__(self, user, password, host, database, schema="public", table=False):
        self.database = database
        self.user = user
        self.password = password
        self.host = host.split(":")[0]
        self.port = "5432" if ':' not in self.host else self.host.split(":")[1]
        self.schema = schema
        self.table = table
        self.conn=psycopg2.connect(database=self.database, user=self.user, port=self.port, password=self.password,
                                host=self.host)
        self.cur=self.conn.cursor()

        self.conn_engine = create_engine("postgresql://%s:%s@%s/%s" % (self.user, self.password,
                                                                       self.host, self.database),encoding='utf-8')

    def __del__(self):
        self.conn.close()
        self.conn.close()


    def db_command_auto(self, sql):
        conn = psycopg2.connect(database=self.database, user=self.user, port=self.port, password=self.password,
                                host=self.host)
        # conn2.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def db_query_engine(self, sql):

        sql = "set search_path to %s;" % self.schema + sql

        df = pd.read_sql(sql, self.conn_engine)
        self.conn_engine.dispose()
        return df


    def db_query(self,sql):
        sql = "set search_path to %s;" % self.schema + sql
        self.cur.execute(sql)
        self.conn.commit()
        result=self.cur.fetchall()

        return result


    def db_write(self, df, tb_name, datadict=None, if_exists='replace'):

        def sqlcol(dfparam, text=None):

            dtypedict = {}
            for i, j in zip(dfparam.columns, dfparam.dtypes):

                if "object" in str(j):
                    if text == "postgresql-text":
                        dtypedict.update({i: TEXT()})
                    else:
                        try:
                            x = int(df[i].str.len().max() / 40) + 1
                        except:
                            x = 50
                        dtypedict.update({i: types.VARCHAR(length=x * 80)})

                if "datetime" in str(j):
                    dtypedict.update({i: types.DateTime()})

                if "float" in str(j):
                    dtypedict.update({i: types.Float(precision=3, asdecimal=True)})

                if "int" in str(j):
                    dtypedict.update({i: types.INT()})

            return dtypedict

        if datadict is None: datadict = sqlcol(df)
        if datadict == 'postgresql-text': datadict = sqlcol(df, 'postgresql-text')

        df.to_sql(tb_name, self.conn_engine, if_exists=if_exists, index=False, schema=self.schema, dtype=datadict)
        self.conn_engine.dispose()

    def db_command(self, sql):
        """db_command 仅仅到数据库"""

        con = psycopg2.connect(database=self.database, user=self.user, port=self.port,
                               password=self.password,host=self.host)

        cur = con.cursor()
        cur.execute(sql)
        con.commit()


if __name__ == '__main__':
    conp=['postgres','since2015','192.168.2.114','credit','credit_quanguo_qy']
    import time
    c1=Persistent(*conp)
    c2 = Transitory(*conp)

    time1=time.time()
    for i in range(1000):
        r=c1.db_query('select pname,credit_code from credit_data_punish limit 1')

        # c1.db_close()
    # print(r)
    time2=time.time()
    #
    time3=time.time()
    for i in range(1000):
        r=c2.db_query('select pname,credit_code from credit_data_punish limit 1')

    time4=time.time()

    time5 = time.time()
    for i in range(1000):
        r = c1.db_query_engine('select pname,credit_code from credit_data_punish limit 1')
    #     # c1.db_close()
    # # print(r)
    #
    time6 = time.time()

    time7 = time.time()
    for i in range(1000):
        r = c2.db_query_engine('select pname,credit_code from credit_data_punish limit 1')
    #
    #
    time8 = time.time()

    print(time2-time1)
    print(time4-time3)

    print(time6-time5)
    print(time8-time7)

    # time.sleep(60)