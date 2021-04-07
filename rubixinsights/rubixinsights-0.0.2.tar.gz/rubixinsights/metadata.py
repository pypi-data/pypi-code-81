from sqlalchemy import create_engine
import pandas as pd
import datetime
from typing import Tuple

class Metadata:
    def __init__(self, 
                host: str,
                port: str,
                username: str,
                password: str,
                database: str,
                data_source: str
                ):
        self.connection_string = self._create_connection_string(host, port, username, password, database)
        self.engine = create_engine(self.connection_string)
        self.table_name = f'metadata_{data_source}'
        self.conn = None
    
    def _create_connection_string(self, host: str, port: str, username: str, password: str, database: str):
        return f"postgres://{username}:{password}@{host}:{port}/{database}"
    
    def _get_connection(self):
        """ Create a singleton connection object """
        if self.conn is None:
            self.conn = self.engine.connect()
        return self.conn

    def report(self) -> pd.DataFrame:
        """ Print out all the related information """
        # read table
        table = pd.read_sql(
            sql = f"select * from {self.table_name}",
            con = self.engine
        )
        return table

    def validate_if_need_the_load(self, account: str, report_name: str, execution_date: datetime.date) -> bool:
        response = self._get_connection().execute(
            f""" 
                 SELECT last_modified
                 FROM {self.table_name} 
                 WHERE account = '{account}' 
                 AND report_name = '{report_name}'
                 AND execution_date = '{execution_date}'
            """
        )
        now = datetime.datetime.utcnow()
        result = response.fetchone()
        if result:
            last_modified = result[0].replace(tzinfo=None)
            return False if  now - last_modified  < datetime.timedelta(days=1) else True
        else:
            return True


    def update_as_succeeded(self, account, report_name, execution_date):
        """Insert metadata or update last_modified when data pulling succeeded
        """
        print('update_as_succeeded')
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self._get_connection().execute(
                f"""
                    INSERT INTO {self.table_name} (account, report_name, execution_date, last_modified)
                    VALUES('{account}', '{report_name}', '{execution_date}', '{now}')
                    ON CONFLICT ON CONSTRAINT unique_constraint 
                    DO UPDATE SET
                        last_modified = excluded.last_modified
                """
            )
        except Exception as e:
            raise e