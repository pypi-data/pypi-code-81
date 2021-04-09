from dotcoin.queries.index import index_markets, index_exchanges
from dotcoin.queries.markets import get_ticker, get_book

from dotcoin.tables.index import table_markets, table_exchanges
from dotcoin.tables.ticker import table_ticker
from dotcoin.tables.book import table_book
from dotcoin.tables.utility import print_table


def print_exchanges(span: int):
    items = index_exchanges()
    table = table_exchanges(items, span=span)
    output = print_table(table)
    print(output)


def print_markets(span: int, compact: bool):
    items = index_markets()
    table = table_markets(items, span=span, compact=compact)
    output = print_table(table)
    print(output)


def print_ticker(exchange: str, quote: str, base: str):
    item = get_ticker(exchange, quote, base)
    table = table_ticker(item)
    output = print_table(table)
    print(output)


def print_book(exchange: str, quote: str, base: str):
    item = get_book(exchange, quote, base)
    table = table_book(item)
    output = print_table(table)
    print(output)
