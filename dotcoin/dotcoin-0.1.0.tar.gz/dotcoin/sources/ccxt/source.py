from typing import List

from dotcoin.core.abstract import Exchange, Source
from dotcoin.sources.ccxt.exchange import CCXTExchange

SUPPORTED = {
    "BINANCE": "binance",
    "BITTREX": "bittrex"
}


class CCXTSource(Source):
    name = "ccxt"

    @staticmethod
    def exchanges() -> List[str]:
        exchanges = list(SUPPORTED.keys())
        return exchanges

    @staticmethod
    def has_exchange(exchange: str) -> bool:
        return exchange in SUPPORTED

    @staticmethod
    def get_exchange(exchange: str) -> Exchange:
        codename = SUPPORTED[exchange]
        return CCXTExchange(exchange, codename)
