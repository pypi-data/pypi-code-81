
import sqlite3

from dbwrapper.sqlite._table import Table
from dbwrapper.sqlite import dtypes
from dbwrapper.sqlite._funcs import Functions

from dbwrapper._util import Navigator, Literal

class Database:
    def __init__(self, conn: sqlite3.Connection, name: str):
        self.conn = conn
        self.name = name
        self.transactions = []
    
    def get_raw(self):
        return None
        
    def close(self):
        pass

    def __str__(self):
        return "sqlite3-database[{0}]".format(self.name)

    def exists(self):
        return self.name in ('main', 'temp')

    @property
    def schema(self):
        cursor = self.conn.execute("SELECT name FROM {0}.sqlite_master WHERE type='table'".format(self.name))
        lst = [x[0] for x in cursor]
        cursor.close()
        return lst

    @property
    def tables(self):
        return Navigator(self, "TableList",
            lambda: self.schema,
            lambda x: self.table(x),
            lambda x: x
        )
    
    @property
    def functions(self):
        return Functions()

    def table(self, name):
        return Table(self.conn, self.name, name)

    def get_current_transaction(self):
        if self.conn and len(self.transactions) > 0:
            return self.transactions[-1]
        else:
            return None

    def start_transaction(self):
        if self.conn:
            tname = "transaction%d" % len(self.transactions)
            self.transactions.append(tname)
            self._ex("SAVEPOINT %s" % tname)
            return tname
    
    def commit(self, tname=None):
        if isinstance(tname, Transaction):
            tname = tname.name

        if self.conn and len(self.transactions) > 0 and (self.transactions[-1] == tname or tname is None):
            self._ex("RELEASE SAVEPOINT %s" % self.transactions[-1])
            return True
        else:
            return False
        
    def rollback(self, tname=None):
        if isinstance(tname, Transaction):
            tname = tname.name

        if self.conn and len(self.transactions) > 0 and (self.transactions[-1] == tname or tname is None):
            self._ex("ROLLBACK TO %s" % self.transactions[-1])
            return True
        else:
            return False

    def __enter__(self):
        self.start_transaction()
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()

    def literal(self, sql):
        return Literal(sql)

    @property
    def dtypes(self):
        return dtypes

    def _ex(self, sql_str, params=[]):
        cursor = self.conn.cursor()
        cursor.execute(sql_str, params)
        lst = list(cursor.fetchall()) if cursor.rowcount > 0 else []
        cursor.close()
        return lst

class Transaction:
    def __init__(self, db, name):
        self.db = db
        self.name = name
    
    def rollback(self):
        return self.db.rollback(self.name)
    
    def commit(self):
        return self.db.commit(self.name)

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()
