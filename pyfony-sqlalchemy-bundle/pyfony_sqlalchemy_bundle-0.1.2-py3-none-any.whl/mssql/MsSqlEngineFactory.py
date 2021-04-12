import urllib.parse
from box import Box
from sqlalchemy import create_engine
from sqlalchemybundle.engine.EngineFactoryInterface import EngineFactoryInterface


class MsSqlEngineFactory(EngineFactoryInterface):
    def create(self, db_config: Box):
        params = urllib.parse.quote_plus(
            f"DRIVER={db_config.driver};"
            f"SERVER={db_config.server};"
            f"DATABASE={db_config.database};"
            f"UID={db_config.username};"
            f"PWD={db_config.password}"
        )

        connection_string = "mssql+pyodbc:///?odbc_connect={}".format(params)

        return create_engine(connection_string, pool_pre_ping=True)

    def get_engine_name(self):
        return "mssql"
