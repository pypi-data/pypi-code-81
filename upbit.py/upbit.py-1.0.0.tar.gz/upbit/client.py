from .api import API
from . import utils
from typing import Optional

class Client(API):
    def get_markets(self, is_details=False) -> list[dict]:
        return super().call_api('get', '/market/all', data={
            'isDetails': is_details
        })

    def get_candles_minutes(self, unit: int = 1, market: str = 'KRW-BTC', to: Optional[str] = None, count: int = 1) -> list[dict]:
        return super().call_api('get', '/candles/minutes/' + str(unit), data={
            'market': market,
            'to': to,
            'count': count
        })

    def get_candles_days(self, market: str = 'KRW-BTC', to: Optional[str] = None, count: int = 1, converting_price_unit: Optional[str] = None) -> list[dict]:
        return super().call_api('get', '/candles/days', data={
            'market': market,
            'to': to,
            'count': count,
            'convertingPriceUnit': converting_price_unit
        })

    def get_candles_weeks(self, market: str = 'KRW-BTC', to: Optional[str] = None, count: int = 1) -> list[dict]:
        return super().call_api('get', '/candles/weeks', data={
            'market': market,
            'to': to,
            'count': count
        })

    def get_candles_months(self, market = 'KRW-BTC', to: Optional[str] = None, count: int = 1) -> list[dict]:
        return super().call_api('get', '/candles/months', data={
            'market': market,
            'to': to,
            'count': count
        })

    def get_trades(self, market: str = 'KRW-BTC', to: Optional[str] = None, count: int = 1, cursor: Optional[str] = None, days_ago: Optional[int] = None) -> list[dict]:
        return super().call_api('get', '/trades/ticks', data={
            'market': market,
            'to': to,
            'count': count,
            'cursor': cursor,
            'daysAgo': days_ago
        })

    def get_ticker(self, markets: list[str] = ['KRW-BTC']) -> list[dict]:
        return super().call_api('get', '/ticker', data={
            'markets': utils.markets_to_str(markets)
        })

    def get_orderbook(self, markets: list[str] = ['KRW-BTC']) -> list[dict]:
        return super().call_api('get', '/orderbook', data={
            'markets': markets,
        })

    def get_accounts(self) -> list[dict]:
        return super().call_api('get', '/accounts', token=True)

    def get_orders_chance(self, market: str = 'KRW-BTC') -> dict:
        return super().call_api('get', '/orders/chance', data={
            'market': market
        }, token=True)

    def get_order(self, uuid: Optional[str] = None, identifier: Optional[str] = None) -> dict:
        return super().call_api('get', '/order', data={
            'uuid': uuid,
            'identifier': identifier
        }, token=True)

    def get_orders(self, market: Optional[str] = None, state: Optional[str] = None, states: Optional[list[str]] = None, uuids: Optional[list[str]] = None, idetifiers: Optional[list[str]] = None, page: int = 1, limit: int = 100, order_by: str = 'desc') -> list[dict]:
        return super().call_api('get', '/orders', data={
            'market': market,
            'state': state,
            'states': states,
            'uuids': uuids,
            'identifiers': idetifiers,
            'page': page,
            'limit': limit,
            'order_by': order_by
        }, token=True)

    def order_cancel(self, uuid: Optional[str] = None, identifier: Optional[str] = None) -> dict:
        return super().call_api('delete', '/order', data={
            'uuid': uuid,
            'identifier': identifier
        }, token=True)

    def order(self, market: str = 'KRW-BTC', side: str = 'bid', volume: Optional[str] = None, price: Optional[str] = None, ord_type: str = 'limit', identifier: Optional[str] = None) -> dict:
        return super().call_api('post', '/orders', data={
            'market': market,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type,
            'identifier': identifier
        }, token=True)

    def get_withdraws(self, currency: Optional[str] = None, state: Optional[str] = None, uuids: Optional[list[str]] = None, txids: Optional[list[str]] = None, limit: int = 100, page: int = 1, order_by: str = 'desc') -> list[dict]:
        return super().call_api('get', '/withdraws', data={
            'currency': currency,
            'state': state,
            'uuids': uuids,
            'txids': txids,
            'limit': limit,
            'page': page,
            'order_by': order_by
        }, token=True)

    def get_withdraw(self, uuid: Optional[str] = None, txid: Optional[str] = None, currency: Optional[str] = None) -> dict:
        return super().call_api('get', '/withdraw', data={
            'uuid': uuid,
            'txid': txid,
            'currency': currency
        }, token=True)

    def get_withdraws_chance(self, currency: str = 'KRW') -> dict:
        return super().call_api('get', '/withdraws/chance', data={
            'currency': currency
        }, token=True)

    def withdraw_coin(self, amount: str, address: str, currency: str = 'KRW', secondary_address: Optional[str] = None, transaction_type: str = 'default') -> dict:
        return super().call_api('post', '/withdraws/coin', data={
            'currency': currency,
            'amount': amount,
            'address': address,
            'secondary_address': secondary_address,
            'transaction_type': transaction_type
        }, token=True)

    def withdraw_krw(self, amount: str) -> dict:
        return super().call_api('post', '/withdraws/krw', data={
            'amount': amount
        }, token=True)

    def get_deposits(self, currency: Optional[str] = None, state: Optional[str] = None, uuids: Optional[list[str]] = None, txids: Optional[list[str]] = None, limit: int = 100 , page: int = 1, order_by: str = 'desc') -> list[dict]:
        return super().call_api('get', '/deposits', data={
            'currency': currency,
            'state': state,
            'uuids': uuids,
            'txids': txids,
            'limit': limit,
            'page': page,
            'order_by': order_by
        }, token=True)

    def get_deposit(self, uuid: Optional[str] = None, txid: Optional[str] = None, currency: Optional[str] = None) -> dict:
        return super().call_api('get', '/deposit', data={
            'uuid': uuid,
            'txid': txid,
            'currency': currency
        }, token=True)

    def generate_coin_address(self, currency: str = 'BTC') -> list[dict]:
        return super().call_api('post', '/deposits/generate_coin_address', data={
            'currency': currency
        }, token=True)

    def get_coin_addresses(self) -> list[dict]:
        return super().call_api('get', '/deposits/coin_addresses', token=True)

    def get_coin_address(self, currency: str = 'BTC') -> dict:
        return super().call_api('get', '/deposits/coin_addresses', data={
            'currency': currency
        }, token=True)

    def deposit_krw(self, amount: str) -> dict:
        return super().call_api('get', '/deposits/krw', data={
            'amount': amount
        }, token=True)

    def get_status_wallet(self, currency: str = 'KRW') -> list[dict]:
        return super().call_api('get', '/status/wallet', data={
            'currency': currency
        }, token=True)

    def get_api_keys(self) -> list[dict]:
        return super().call_api('get', '/api_keys', token=True)
