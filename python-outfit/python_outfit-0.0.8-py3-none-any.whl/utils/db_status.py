from enum import Enum

class MongoLib(Enum):
    """enumeration for mongo libs for python
    """
    MONGO_ALCHEMY = 1
    PYMONGO = 2
    MONGOENGINE = 3


class DBStatus(object):

    def mongo_checker(self, dbmongo, mongo_libs):

        def mongoengine():
            import copy
            result = True, 'mongo using mongoengine ok'
            try:
                temp_dbmongo = copy.copy(dbmongo)

                class TestConn(temp_dbmongo.Document):
                    test = temp_dbmongo.StringField()

                temp = TestConn.objects()
                result = True, 'mongo using mongoengine is working'
            except AttributeError as atr:
                result = False, 'mongo using mongoengine not found'
            return result

        def pymongo():
            import copy 
            result = True, 'mongo using pymongo ok' 
            try:
                temp_dbmongo = copy.copy(dbmongo)
                temp_dbmongo.db.test_conn.find({})
                result = True, 'mongo using pymongo is working'
            except AttributeError as atr:
                result = False, 'mongo using pymongo not found'
            return result

        list_lib = [None, pymongo, mongoengine]
        result = []
        for m in mongo_libs:
            result = list_lib[m.value - 1] if m != None else False, 'mongo driver is not found'

        return result

    def sql_checker(self, db, dbprovider):
        def sql_alchemy():
            try:
                db.engine.execute('SELECT 1')
                return True, dbprovider + ' Database is ok' 
            except :
                return False, dbprovider + ' is not working'

        return sql_alchemy

    def mysql_checker(self, db):
        return self.sql_checker(db, 'MySQL')

    def pgsql_checker(self, db):
        return self.sql_checker(db, 'Postgres')
