from abc import abstractmethod

class BaseDiscriminator():
    @abstractmethod
    def match(self, url: str) -> bool:
        pass