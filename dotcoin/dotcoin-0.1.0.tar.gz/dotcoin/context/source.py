from typing import Dict, List

from dotcoin.core.abstract import Exchange, Source
from dotcoin.core.error import InvalidSourceError
from dotcoin.sources import all_sources

_exchange_source_map_ = {}


def _source_map() -> Dict[str, Source]:
    if not _exchange_source_map_:
        for source in all_sources():
            for name in source.exchanges():
                if name not in _exchange_source_map_:
                    _exchange_source_map_[name] = source
    return _exchange_source_map_


def all_exchanges() -> List[Exchange]:
    return [source.get_exchange(name) for name, source in _source_map().items()]


def has_exchange(exchange: str) -> bool:
    return exchange in _source_map()


def get_exchange(exchange: str) -> Exchange:
    if has_exchange(exchange):
        source: Source = _source_map().get(exchange)
        return source.get_exchange(exchange)
    raise InvalidSourceError(f'"{exchange}" is not a supported exchange.')
