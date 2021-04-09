from typing import List

from dotcoin.core.types import Market
from dotcoin.context.source import all_exchanges, get_exchange
from dotcoin.queries.markets import all_markets
from dotcoin.queries.utility import exchanges_to_names


def index_exchanges() -> List[str]:
    return exchanges_to_names(all_exchanges())


def index_markets() -> List[Market]:
    markets = all_markets()
    return sorted(markets, key=str)


def index_markets_from(exchange: str) -> List[Market]:
    _exchange = get_exchange(exchange)
    markets = _exchange.markets()
    return sorted(markets, key=str)
