from typing import List, Iterator
from collections import Counter

from dotcoin.core.types import Market
from dotcoin.core.abstract import Exchange


def match_markets(exchanges: List[Exchange]) -> Iterator[Market]:
    counter = Counter()
    for exchange in exchanges:
        markets = exchange.markets()
        counter.update(markets)

    quota = len(exchanges)
    return filter(lambda match: counter[match] is quota, counter)


def match_exchanges(market: Market, exchanges: List[Exchange]) -> Iterator[Exchange]:
    return filter(lambda exchange: exchange.has_market(market), exchanges)
