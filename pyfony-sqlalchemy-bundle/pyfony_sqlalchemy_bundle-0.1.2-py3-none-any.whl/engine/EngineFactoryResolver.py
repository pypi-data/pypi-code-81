from typing import List
from box import Box
from sqlalchemybundle.engine.EngineFactoryInterface import EngineFactoryInterface


class EngineFactoryResolver:
    def __init__(self, engine_factories: List[EngineFactoryInterface]):
        self.__engine_factories = engine_factories

    def resolve(self, db_config: Box) -> EngineFactoryInterface:
        for engine_factory in self.__engine_factories:
            if engine_factory.get_engine_name() == db_config.engine:
                return engine_factory

        raise Exception(f"No engine factory found for engine: {db_config.engine}")
