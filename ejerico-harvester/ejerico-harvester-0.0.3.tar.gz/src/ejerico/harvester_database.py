"""TODO doc"""

import hashlib
import os
import sys
import threading
import time
import uuid

import sqlite3

from datetime import datetime
from pathlib import Path

from ejerico_sdk.annotations import singleton

__all__ = ["HarvesterDatabase"]

@singleton
class HarvesterDatabase(object):

    def __init__(self):
        self._db = self._getHarvesterInternalDB()
        self._key_lock = threading.Lock()

    def isNewOrUpdated(self, uri=None, updated=None, hash=None):
        if self._db is None: return True
        if uri is None: return False

        rst = False

        self._key_lock.acquire()
        try:
            my_uri = hashlib.sha1(bytes(uri, "ascii")).hexdigest()
            
            sql = SQL_QUERY_RESOURCE_BY_URI.format(my_uri)

            cur = self._db.cursor()
            cur.execute(sql)
            
            rows = cur.fetchall()
            for row_id,row_uri,row_updated,row_mimetype,row_hash in rows:
                if updated is not None:
                    rst =  rst or (row_updated < datetime.timestamp(updated))
                if hash is not None:
                    rst =  rst or (row_hash != hash)
            else:
                rst = rst or (0 == len(rows))
        except sqlite3.Error as e:
            print("[HarvesterDatabase::isNewOrUpdated] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release()    
        
        return rst

    def markAsVisited(self, uri=None, visited=None):
        if self._db is None: return
        if uri is None: return

        self._key_lock.acquire()
        try:
            my_uri = hashlib.sha1(bytes(uri, "ascii")).hexdigest()
            visited = visited if visited is not None else int(datetime.now().timestamp())

            sql = SQL_INSERT_OR_UPDATE_RESOURCE_VISITED.format(visited, my_uri)

            cur = self._db.cursor()
            cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as e:
            print("[HarvesterDatabase::markAsVisited] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release() 

    def markAsUpdated(self, uri=None, updated=None, visited=None, hash=None, mimetype=None):
        if self._db is None: return
        if uri is None: return

        self._key_lock.acquire()
        try:
            my_uri = hashlib.sha1(bytes(uri, "ascii")).hexdigest()
            updated = int(datetime.timestamp(updated)) if updated is not None else 0
            visited = visited if visited is not None else int(datetime.now().timestamp())
            hash = "'{}'".format(hash) if hash else "NULL"
            mimetype = "{}".format(mimetype) if mimetype else "NULL"
            
            sql = SQL_INSERT_OR_UPDATE_RESOURCE.format(my_uri, mimetype, hash, updated, visited)

            cur = self._db.cursor()
            cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as e:
            print("[HarvesterDatabase::markAsUpdated] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release() 

    def getObsoleteResources(self, visited):
        if self._db is None: return []
        
        rst = []
        if isinstance(visited, int):
            self._key_lock.acquire()
            try:
                sel = SQL_QUERY_RESOURCE_BY_OBSOLETE_VISITED,format(visited)

                cur = self._db.cursor()
                cur.execute(sql)

                rst = cur.fetchall()
            except sqlite3.Error as e:
                print("[HarvesterDatabase::getObsoletesResources] error accessing db -> {}".format(e))
            finally:    
                self._key_lock.release()
        return rst
        
    def deleteObsoleteResource(self, uri):
        if self._db is None: return
        if uri is None: return 

        self._key_lock.acquire()
        try:
            my_uri = hashlib.sha1(bytes(uri, "ascii")).hexdigest()

            sql = SQL_DELETE_RESOURCE_BY_URI.format(my_uri)

            cur = self._db.cursor()
            cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as e:
            print("[HarvesterDatabase::getObsoletesResources] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release()
    
    def query(self, statement):
        if self._db is None: return
        if statement is None: return 

        rows = []
        self._key_lock.acquire()
        try:
            cur = self._db.cursor()
            cur.execute(statement)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print("[HarvesterDatabase::query] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release()
        return rows
    

    def execute(self, *statements):
        if self._db is None: return
        if statements is None: return 

        self._key_lock.acquire()
        try:
            cur = self._db.cursor()
            for statement in statements:
                cur.execute(statement)
            self._db.commit()
        except sqlite3.Error as e:
            print("[HarvesterDatabase::execute] error accessing db -> {}".format(e))
        finally:    
            self._key_lock.release()

    def _getPathHarvesterInternalDB(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            path = "{}{}.ejerico".format(str(Path.home()), os.sep)
            os.makedirs(path, exist_ok=True)
            path = "{}{}harvester.db".format(path, os.sep)
            return path
        elif sys.platform == "darwin":
            path = "{}{}.ejerico".format(str(Path.home()), os.sep)
            os.makedirs(path, exist_ok=True)
            path = "{}{}harvester.db".format(path, os.sep)
            return path
            #return [os.environ.get('OSX_XYZ')]
        elif sys.platform == "win32":
            return [os.environ.get('WIN_XYZ')]

    def _getHarvesterInternalDB(self):
        db = None
        
        path = self._getPathHarvesterInternalDB()
        try:
            db = sqlite3.connect(path, check_same_thread=False)
            c = db.cursor()
            c.execute(SQL_CREATE_RESOURCE_TABLE)
            c.execute(SQL_CREATE_RESOURCE_INDEX_URI)
            c.execute(SQL_CREATE_RESOURCE_INDEX_VISITED)
            db.commit()
        except sqlite3.Error as e:
            print("[_getHarvesterInternalDB] error opening harvester internal db ({}): {}".format(path, e))

        return db

##############################################################################
# SQL STATEMENTS 
##############################################################################

SQL_CREATE_RESOURCE_TABLE = '''
    CREATE TABLE IF NOT EXISTS "resources" (
        "id"	    INTEGER PRIMARY KEY AUTOINCREMENT,
        "updated"	INTEGER NOT NULL,
        "visited"	INTEGER NOT NULL,
        "uri"	    TEXT NOT NULL UNIQUE,
        "mimetype"  TEXT,
        "hash"	    TEXT
    )
'''
SQL_CREATE_RESOURCE_INDEX_URI = '''
    CREATE INDEX IF NOT EXISTS "resource_uri" ON "resources" (
        "uri"
    )
'''
SQL_CREATE_RESOURCE_INDEX_VISITED = '''
    CREATE INDEX IF NOT EXISTS "resource_uri" ON "resources" (
        "visited"
    )
'''

SQL_QUERY_RESOURCE_BY_URI = '''
    SELECT id, uri, updated, mimetype, hash FROM "resources" WHERE uri =\'{}\'
'''
SQL_QUERY_RESOURCE_BY_VISITED = '''
    SELECT id, uri, updated, mimetype, hash FROM "resources" WHERE visited = {}
'''
SQL_QUERY_RESOURCE_BY_OBSOLETE_VISITED = '''
    SELECT id FROM "resources" WHERE visited < {}
'''

SQL_INSERT_OR_UPDATE_RESOURCE = '''
    REPLACE INTO "resources" ("uri", "mimetype", "hash", "updated", "visited")
    VALUES('{}', '{}', {}, {}, {});
'''
SQL_INSERT_OR_UPDATE_RESOURCE_VISITED = '''
    UPDATE "resources" 
    SET "visited" = {}, "updated" = "updated"
    WHERE "uri" = '{}';
'''

SQL_DELETE_RESOURCE_BY_URI = '''
    DELETE "resources" WHERE uri =\'{}\'
'''
SQL_DELETE_RESOURCE_BY_VISITED = '''
    DELETE "resources" WHERE visited < {}
'''
