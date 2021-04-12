from abc import ABC, abstractmethod


class DecoratorMappingInterface(ABC):
    @abstractmethod
    def get_mapping(self) -> dict:
        pass
