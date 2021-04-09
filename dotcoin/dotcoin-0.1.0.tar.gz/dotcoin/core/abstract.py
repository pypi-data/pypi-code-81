from abc import ABC, abstractmethod
from typing import List

from dotcoin.core.types import Market, Ticker, Book


class Exchange(ABC):
    name: str = None
    source: str = None

    @abstractmethod
    def markets(self) -> List[Market]:
        raise NotImplementedError

    @abstractmethod
    def has_market(self, market: Market) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_ticker(self, market: Market) -> Ticker:
        raise NotImplementedError

    @abstractmethod
    def get_book(self, market: Market) -> Book:
        raise NotImplementedError


class Source(ABC):
    name: str = None

    @staticmethod
    @abstractmethod
    def exchanges() -> List[str]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def has_exchange(exchange: str) -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_exchange(exchange: str) -> Exchange:
        raise NotImplementedError
