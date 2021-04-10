
import psycopg2
from psycopg2 import extensions
import weakref

from dbwrapper.postgresql._db import Database

MASTER_DB="postgres"
TEMP_DB="temp"

class Connection:
    def __init__(self, *args, **kwargs):
        self.target = (args, kwargs)
        self.dbs = weakref.WeakSet()
    
    def database(self, name):
        db = Database(self.target, name)
        self.dbs.add(db)
        return db

    def start_transaction(self):
        for db in self.dbs:
            db.start_transaction()
    
    def commit(self):
        for db in self.dbs:
            db.commit()
        
    def rollback(self):
        for db in self.dbs:
            db.rollback()

    def __enter__(self):
        self.start_transaction()
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()

    def __str__(self):
        return "postgresql-connection[Target=%s@%s,Opened=%s]" % (
            self.target[1].get("user", "unknown"),
            self.target[1].get("host", "localhost"),
            self.is_open()
        )

    def get_raw(self):
        return None

    def is_open(self):
        return len(self.dbs) > 0

    def open(self):
        for db in self.dbs:
            db.open()

    def close(self):
        for db in self.dbs:
            db.close()
