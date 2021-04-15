from abc import abstractmethod
from typing import List

class BaseSearchEngine():
    @abstractmethod
    def search(self, query:str, number:int = 10) -> List[str]:
        pass
