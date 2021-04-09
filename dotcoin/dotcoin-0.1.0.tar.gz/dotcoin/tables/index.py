from typing import List

from dotcoin.core.types import Table, Market
from dotcoin.tables.utility import KeyTable


def table_exchanges(exchanges: List[str], span: int = 3) -> Table:
    headers = ['Init.', 'Exchanges']

    content = KeyTable(headers, exchanges)
    content.set_key(lambda word: word[0])
    content.build(span)

    return content.get_table()


def table_markets(markets: List[Market], span: int = 3, compact: bool = False) -> Table:
    headers = ['Quote', 'Base']

    content = KeyTable(headers, markets)
    content.set_key(lambda market: market.quote)
    if compact:
        content.set_parser(lambda market: f"{market.base}")
    else:
        content.set_parser(lambda market: f"{market.base}/{market.quote}")
    content.build(span)

    return content.get_table()
