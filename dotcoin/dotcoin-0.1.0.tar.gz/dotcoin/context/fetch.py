from dotcoin.core.error import InvalidSourceError, InvalidContextError
from dotcoin.core.types import Market, Ticker, Book
from dotcoin.context.source import has_exchange, get_exchange


def fetch_ticker(exchange: str, market: Market) -> Ticker:
    if has_exchange(exchange):
        _exchange = get_exchange(exchange)
        if _exchange.has_market(market):
            return _exchange.get_ticker(market)
        raise InvalidContextError(f'"{market}" is not supported for this exchange.')
    raise InvalidSourceError(f'"{exchange}" is not a supported exchange.')


def fetch_book(exchange: str, market: Market) -> Book:
    if has_exchange(exchange):
        _exchange = get_exchange(exchange)
        if _exchange.has_market(market):
            return _exchange.get_book(market)
        raise InvalidContextError(f'"{market}" is not supported for this exchange.')
    raise InvalidSourceError(f'"{exchange}" is not a supported exchange.')
