from py3db.log.Log import Log
from pymysql import connect


class MySql:
    def __init__(self, ip, user_name, password, database):
        self.ip = ip
        self.user_name = user_name
        self.password = password
        self.database = database
        self.db = None
        self.log = Log("mysql.log")
        self.create_connect()

    def __str__(self) -> str:
        return ("ip:{0}\n"
                + "user_name:{1}\n"
                + "password:{2}\n"
                + "py3db:{3}\n"
                + "db:{4}\n").format(
            self.ip,
            self.user_name,
            self.password,
            self.database,
            self.db
        )

    def create_connect(self):
        try:
            self.db = connect(
                host=self.ip,
                user=self.user_name,
                password=self.password,
                db=self.database,
                charset='utf8mb4'
            )
            if not self.db:
                self.log.call_error("mysql.log")
        except Exception as e:
            self.log.call_error()
            self.log.error(str(e))

    def close_connect(self):
        try:
            self.db.close()
        except Exception as e:
            self.log.call_error()
            self.log.error(str(e))

    def operation_database(self, sql, variable_name=None, variable=None):
        print(sql)
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.log.call_error()
            self.log.error("{0} {1} {2}".format(
                e, variable_name, variable
            ))

    def __del__(self):
        if not self.db and not self:
            self.db.close_connect()


if __name__ == "__main__":
    mysql = MySql("localhost", "root", "111", "sex")
