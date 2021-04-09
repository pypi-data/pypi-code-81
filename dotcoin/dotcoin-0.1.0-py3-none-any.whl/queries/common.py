from typing import List

from dotcoin.core.types import Market
from dotcoin.context.match import match_markets, match_exchanges
from dotcoin.context.source import all_exchanges
from dotcoin.queries.utility import exchanges_to_names, names_to_exchanges


def common_exchanges(quote: str, base: str) -> List[str]:
    market = Market(quote.upper(), base.upper())
    matches = match_exchanges(market, all_exchanges())
    names = exchanges_to_names(matches)
    return sorted(names)


def common_markets(exchanges: List[str]) -> List[Market]:
    _exchanges = names_to_exchanges(exchanges)
    matches = match_markets(_exchanges)
    return sorted(matches, key=str)
