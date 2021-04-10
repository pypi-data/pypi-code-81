
import sqlite3

from dbwrapper.sqlite._db import Database

MASTER_DB="main"
TEMP_DB="temp"

class Connection:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)
        self.conn.isolation_level = None
        self.file = file

        self.conn.execute("PRAGMA read_uncommitted = true;")
    
    def database(self, name):
        if self.conn:
            return Database(self.conn, name)

    def start_transaction(self):
        if self.conn:
            self.conn.execute("BEGIN")
    
    def commit(self):
        if self.conn:
            self.conn.execute("COMMIT")
        
    def rollback(self):
        if self.conn:
            self.conn.execute("ROLLBACK")

    def __enter__(self):
        self.start_transaction()
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()

    def __str__(self):
        return "sqlite3-connection[File=%s,Opened=%s]" % (self.file, self.conn is not None)

    def get_raw(self):
        return self.conn

    def is_open(self):
        return self.conn is not None

    def open(self):
        if not self.conn:
            self.conn = sqlite3.connect(file)
            self.conn.isolation_level = None
            return True
        else:
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            return True
        else:
            return False
