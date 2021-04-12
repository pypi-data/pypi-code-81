from abc import ABC, abstractmethod
from typing import Callable, Dict


class ViewInteractor(ABC):
    @abstractmethod
    def set_callbacks(self, callbacks: Dict[str, Callable]):
        raise NotImplementedError

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError
