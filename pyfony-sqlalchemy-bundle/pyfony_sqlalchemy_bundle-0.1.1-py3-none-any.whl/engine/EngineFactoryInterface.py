from abc import ABC, abstractmethod
from box import Box


class EngineFactoryInterface(ABC):
    @abstractmethod
    def create(self, db_config: Box):
        pass

    @abstractmethod
    def get_engine_name(self):
        pass
