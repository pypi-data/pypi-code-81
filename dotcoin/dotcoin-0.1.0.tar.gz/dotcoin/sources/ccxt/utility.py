from typing import List

from dotcoin.core.types import Market, Context, Ticker, Order, Book


def market_to_symbol(market: Market) -> str:
    return f"{market.base}/{market.quote}"


def symbol_to_market(symbol: str) -> Market:
    base, quote = symbol.split("/")
    return Market(quote, base)


def many_symbols_to_markets(symbols: list) -> List[Market]:
    return list(map(symbol_to_market, symbols))


TICKER_KEYMAP = {'bid': 'bid', 'ask': 'ask', 'last': 'last', 'volume': 'baseVolume', 'var': 'percentage'}


def parse_ticker(context: Context, ticker: dict) -> Ticker:
    str_dict = {next_key: ticker[old_key] for next_key, old_key in TICKER_KEYMAP.items()}
    num_dict = {key: float(value) for key, value in str_dict.items()}
    return Ticker(context, **num_dict)


def parse_order(item: list) -> Order:
    price, base = item
    return Order(price * base, base, price)


def parse_book(context: Context, book: dict) -> Book:
    bids = list(map(parse_order, book['bids']))
    asks = list(map(parse_order, book['asks']))
    return Book(context, bids, asks)
