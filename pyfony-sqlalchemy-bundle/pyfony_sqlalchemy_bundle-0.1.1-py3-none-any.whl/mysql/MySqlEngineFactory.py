from box import Box
from sqlalchemy import create_engine
from sqlalchemybundle.engine.EngineFactoryInterface import EngineFactoryInterface


class MySqlEngineFactory(EngineFactoryInterface):
    def create(self, db_config: Box):
        connection_string = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
            db_config.username,
            db_config.password,
            db_config.host,
            db_config.port if "port" in db_config else 3306,
            db_config.database,
        )

        return create_engine(connection_string)

    def get_engine_name(self):
        return "mysql"
