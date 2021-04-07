from abc import abstractmethod
from typing import Optional

from CryptoPrice.retrievers.AbstractRetriever import AbstractRetriever
from CryptoPrice.common.prices import Price


class PriceRetriever(AbstractRetriever):

    def __init__(self, name: str):
        super().__init__(name)

    def _get_closest_price(self, asset: str, ref_asset: str, timestamp: int) -> Optional[Price]:
        price = self.get_local_price(asset, ref_asset, timestamp)
        return price

    @abstractmethod
    def get_online_price(self, timestamp: int):
        raise NotImplementedError

    def get_local_price(self, asset, ref_asset, timestamp) -> Optional[Price]:
        pass