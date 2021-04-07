import os
import psycopg2
import psycopg2.extras as _extras
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from io import StringIO


# https://www.psycopg.org/docs/usage.html#
# https://www.psycopg.org/docs/usage.html#with-statement
# https://docs.sqlalchemy.org/en/14/core/engines.html#postgresql
# https://docs.sqlalchemy.org/en/13/core/connections.html#calling-stored-procedures
# https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
# https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
# https://stackoverflow.com/questions/1547145/defining-private-module-functions-in-python

class _Credentials:

    def __init__(self):
        mode = os.environ.get('MODE')

        if not mode:
            load_dotenv()
        mode = os.environ['MODE']

        self.host = os.environ[f"DB_HOST_{mode}"]
        self.port = os.environ[f"DB_PORT_{mode}"]
        self.database = os.environ[f"DB_DATABASE_{mode}"]
        self.user = os.environ[f"DB_USER_{mode}"]
        self.pw = os.environ[f"DB_PASSWORD_{mode}"]


# _cred = _Credentials()
def _get_credentials():
    return _Credentials()


def engine_url():
    cred = _get_credentials()
    return 'postgresql://{}:{}@{}:{}/{}'.format(cred.user,
                                                cred.pw,
                                                cred.host,
                                                cred.port,
                                                cred.database)


#_engine = create_engine(_engine_url)
def engine():
    return create_engine(engine_url())


class Connection:

    def __init__(self, connection=None):
        self.connection = connection

    def __enter__(self):
        '''When connection block is entered a connection is openend.
        With leaving the with block, if no exception has been raised by the block,
        the transaction is committed. In case of a exception the transaction is rolled back.
        In both cases the connection is closed.'''

        cred = _get_credentials()
        
        self.connection = psycopg2.connect(host=cred.host,
                                           port=cred.port,
                                           database=cred.database,
                                           user=cred.user,
                                           password=cred.pw)

        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()

        self.connection.close()


def _get_cols(cols):
    """generate comma sperated string with column names"""
    return ','.join(('"{}"'.format(x) for x in list(cols)))


def _generate_insert_sql(df, table, schema):
    """generate raw insert sql"""
    cols = _get_cols(df.columns)
    placeholder = ','.join(['%s'] * len(df.columns))
    sql = f"INSERT INTO {schema}.{table}({cols}) VALUES ({placeholder})"

    return sql


def _generate_insert_sql_execute_values(df, table, schema):
    """generate raw insert sql for bulk insert=> must contain a single %s placeholder"""
    cols = _get_cols(df.columns)
    sql = f"INSERT INTO {schema}.{table}({cols}) VALUES %s"

    return sql


def insert_returning(df, table, schema, con, col='ID'):
    """inserts first row of a dataframe and returns primary key"""

    if len(df) > 1:
        raise AssertionError('RETURNING after INSERT works only for one record')

    if df.empty:
        return

    sql = _generate_insert_sql(df, table, schema)
    sql += f" RETURNING {col}"

    with con.cursor() as cur:
        data = list(df.itertuples(index=False, name=None))[0]  # get first row as tuple
        cur.execute(sql, data)
        val = cur.fetchone()[0]
        return val


def bulk_insert(df, table, schema, con):
    """"bulk inserts dataframes"""

    if df.empty:
        return

    data = [list(row) for row in df.itertuples(index=False)]  # get rows as list of lists

    with con.cursor() as cur:
        # method 1: execute many => slow
        # sql = generate_insert_sql(df, table, schema)
        # cur.executemany(sql, data)

        # method 2: copy from buffer => fast, but df must contain all columns from database table => not flexible
        # buffer = StringIO()
        # df.to_csv(buffer, index=False, header=False)
        # buffer.seek(0)
        # cur.copy_from(buffer, f"{schema}.{table}", sep=",")

        # method 3: execute_values
        sql = _generate_insert_sql_execute_values(df, table, schema)
        _extras.execute_values(cur, sql, data)


def to_sql(df, table, schema, if_exists='append', index=False, ):
    """helper function to avoid repeating parameters"""
    df.to_sql(table, engine(), schema=schema, if_exists=if_exists, index=index)
