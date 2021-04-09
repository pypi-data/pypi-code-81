from typing import List

import ccxt

from dotcoin.core.abstract import Exchange
from dotcoin.core.types import Market, Context, Ticker, Book
from dotcoin.sources.ccxt.utility import many_symbols_to_markets, parse_ticker, parse_book, market_to_symbol


class CCXTExchange(Exchange):
    source = "CCXT"

    def __init__(self, name: str, code: str):
        self.name = name
        self._ccxt_exchange: ccxt.Exchange = getattr(ccxt, code)()
        self._ccxt_exchange.load_markets()

    def markets(self) -> List[Market]:
        ccxt_symbols = self._ccxt_exchange.markets.keys()
        markets = many_symbols_to_markets(ccxt_symbols)
        return markets

    def has_market(self, market: Market) -> bool:
        ccxt_symbol = market_to_symbol(market)
        return ccxt_symbol in self._ccxt_exchange.markets

    def get_ticker(self, market: Market) -> Ticker:
        ccxt_symbol = market_to_symbol(market)
        raw_ticker = self._ccxt_exchange.fetch_ticker(ccxt_symbol)

        context = Context(market, self.name)
        ticker = parse_ticker(context, raw_ticker)
        return ticker

    def get_book(self, market: Market) -> Book:
        ccxt_symbol = market_to_symbol(market)
        raw_book = self._ccxt_exchange.fetch_l2_order_book(ccxt_symbol)

        context = Context(market, self.name)
        return parse_book(context, raw_book)
