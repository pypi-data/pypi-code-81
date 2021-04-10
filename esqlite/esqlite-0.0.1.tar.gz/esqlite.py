"""
esqlite means 'easy sqlite', is a sqlite3 wrapper.
method 'execute' for execute any SQL and return result set.
method 'batch_save' for batch insert dict list data. Table will be created if the table not exists.
"""
import sqlite3


class DB:

    def __init__(self, database):
        """
        constructor

        :param database: database name
        """
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = self._dict_factory

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=None, commit=True):
        """
        execute SQL statement

        sql: SQL statement
        args: SQL statement args, list type
        autocommit: if commit transaction
        Returns: result set
        """
        cursor = self._connection.cursor()
        if args is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        result_set = cursor.fetchall()
        cursor.close()
        return result_set

    def batch_save(self, table, dict_list, cleanup=False):
        """
        save dict list data to db, default init table with dict keys if table not exists

        :param table: table name
        :param dict_list: dict list data
        :param cleanup: delete old data in the table before insert data
        :return:
        """
        if not dict_list:
            return
        column_names = dict_list[0].keys()
        cursor = self._connection.cursor()
        # create table
        if cleanup:
            cursor.execute(f'drop table if exists {table}')
        cursor.execute(f'''create table if not exists {table}({','.join(column_names)})''')
        # insert data
        sql = f'''insert into {table}({', '.join(column_names)}) values ({', '.join(['?' for _ in range(len(column_names))])})'''
        for row in dict_list:
            values = [row.get(column_name, None) for column_name in column_names]
            cursor.execute(sql, values)
        self._connection.commit()
        cursor.close()


if __name__ == '__main__':
    db = DB('test.db')
    data = [{'id': 1, 'name': 'Bob'}, {'id': 2, 'name': 'Lena'}]
    # batch save, default init table with dict keys
    db.batch_save('user', data, cleanup=True)
    # insert
    db.execute('insert into user(id, name) values (?,?)', [3, 'C++'])
    print(db.execute('select * from user'))
    # update
    db.execute('update user set name=? where id=?', ['Python', 3])
    print(db.execute('select * from user'))
    # delete
    db.execute('delete from user where id=?', [3])
    # find
    print(db.execute('select * from user order by id desc'))
