from typing import Iterator, List

from dotcoin.core.abstract import Exchange
from dotcoin.context.source import get_exchange


def exchanges_to_names(exchanges: Iterator[Exchange]) -> List[str]:
    return [getattr(exchange, 'name') for exchange in exchanges]


def names_to_exchanges(names: Iterator[str]) -> List[Exchange]:
    return [get_exchange(name.upper()) for name in names]
