class SQLite:

    def __init__(self, cursor):
        self.cursor = cursor

    def get(self, table, keyname, keyvalue):
        self.cursor.execute(F"SELECT * FROM `{table}` WHERE `{keyname}` = '{keyvalue}';")
        return self.cursor.fetchone()
