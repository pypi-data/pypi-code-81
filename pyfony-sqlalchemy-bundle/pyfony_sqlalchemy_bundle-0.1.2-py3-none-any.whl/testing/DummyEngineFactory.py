from box import Box
from sqlalchemybundle.engine.EngineFactoryInterface import EngineFactoryInterface


class DummyEngineFactory(EngineFactoryInterface):
    def create(self, db_config: Box):
        return "dummyengine"

    def get_engine_name(self):
        return "dummy"
