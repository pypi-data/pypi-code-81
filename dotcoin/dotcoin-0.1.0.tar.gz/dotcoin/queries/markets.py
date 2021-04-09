from typing import List

from dotcoin.context.fetch import fetch_ticker, fetch_book
from dotcoin.context.source import all_exchanges
from dotcoin.core.types import Market, Ticker, Book


def all_markets() -> List[Market]:
    markets = set()
    for exchange in all_exchanges():
        markets.update(exchange.markets())
    return list(markets)


def get_ticker(exchange: str, quote: str, base: str) -> Ticker:
    market = Market(quote.upper(), base.upper())
    return fetch_ticker(exchange.upper(), market)


def get_book(exchange: str, quote: str, base: str) -> Book:
    market = Market(quote.upper(), base.upper())
    return fetch_book(exchange.upper(), market)
