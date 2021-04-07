"""
@author  : MG
@Time    : 2020/10/9 12:00
@File    : __init__.py.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import enum
import time
from datetime import datetime, timedelta
from functools import partial, lru_cache
from threading import Thread
from typing import List, Sequence, Callable
from unittest import mock

from ibats_utils.mess import datetime_2_str
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.database import database_manager
from vnpy.trader.database.database_sql import SqlManager
from vnpy.trader.object import BarData

from vnpy_extra.db.md_reversion_rights import get_symbol_marked_main_or_sec


def check_datetime_trade_available(dt: datetime) -> bool:
    """判断可发送交易请求的时间段（中午11:30以后交易）"""
    hour = dt.hour
    minute = dt.minute
    is_available = 0 <= hour < 3 or 9 <= hour <= 10 or (11 == hour and minute < 30) or 13 <= hour < 15 or (21 <= hour)
    return is_available


def check_datetime_available(dt: datetime) -> bool:
    hour = dt.hour
    is_available = 0 <= hour < 3 or 9 <= hour < 15 or 21 <= hour
    return is_available


class CrossLimitMethod(enum.IntEnum):
    open_price = 0
    mid_price = 1
    worst_price = 2


class CleanupOrcaServerProcessIntermittent(Thread):

    def __init__(self, sleep_time=5, interval=1800):
        super().__init__()
        self.is_running = True
        self.interval = interval
        self.sleep_time = sleep_time
        self.sleep_count = interval // sleep_time

    def run(self) -> None:
        from plotly.io._orca import cleanup
        count = 0
        while self.is_running:
            time.sleep(self.sleep_time)
            count += 1
            if count % self.sleep_count == 0 or not self.is_running:
                cleanup()
                count = 0


DEFAULT_STATIC_ITEMS = [
    "available", "info_ratio",
    "max_new_higher_duration", "daily_trade_count", "return_drawdown_ratio",
    "image_file_url",
    "strategy_class_name", "id_name", "symbols", "cross_limit_method", "backtest_status",
]

STOP_OPENING_POS_PARAM = "stop_opening_pos"
ENABLE_COLLECT_DATA_PARAM = "enable_collect_data"


class StopOpeningPos(enum.IntEnum):
    open_available = 0
    stop_opening_and_log = 1
    stop_opening_and_nolog = 2


def do_nothing(*args, **kwargs):
    """空函数"""
    return


# 加载主力连续合约
@lru_cache()
def mock_load_bar_data(
        _self: SqlManager,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime,
        write_log_func: Callable = None,
) -> Sequence[BarData]:
    # 整理参数
    if isinstance(start, datetime):
        start = start.replace(minute=0, second=0, microsecond=0)

    if isinstance(end, datetime):
        end = end.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    if write_log_func is None:
        write_log_func = do_nothing

    if symbol.find('9999') == -1 and symbol.find('8888') == -1:
        main_symbol = get_symbol_marked_main_or_sec(symbol, is_main=True)
        s = (
            _self.class_bar.select().where(
                (_self.class_bar.symbol == main_symbol)
                & (_self.class_bar.exchange == exchange.value)
                & (_self.class_bar.interval == interval.value)
                & (_self.class_bar.datetime >= start)
                & (_self.class_bar.datetime <= end)
            ).order_by(_self.class_bar.datetime)
        )

        data: List[BarData] = [db_bar.to_bar() for db_bar in s]
        data_len = len(data)
        if data_len > 0:
            latest_dt = max([_.datetime for _ in data])
            write_log_func(f"加载主力连续合约 {main_symbol} {data_len}条 "
                           f"[{datetime_2_str(start)} ~ {datetime_2_str(latest_dt)}]")
            start = latest_dt + timedelta(minutes=1)
        else:
            write_log_func(f"加载主力连续合约 {main_symbol} {0}条 "
                           f"[{datetime_2_str(start)} ~ {datetime_2_str(end)}]")
    else:
        data = []
        data_len = 0

    s = (
        _self.class_bar.select().where(
            (_self.class_bar.symbol == symbol)
            & (_self.class_bar.exchange == exchange.value)
            & (_self.class_bar.interval == interval.value)
            & (_self.class_bar.datetime >= start)
            & (_self.class_bar.datetime <= end)
        ).order_by(_self.class_bar.datetime)
    )

    data_sub: List[BarData] = [db_bar.to_bar() for db_bar in s]
    data.extend(data_sub)
    if symbol.find('9999') == -1 and symbol.find('8888') == -1:
        data_sub_len = len(data_sub)
        write_log_func(f"加载当期合约 {symbol} {data_sub_len}条 累计 {data_len + data_sub_len} 条"
                       f"[{datetime_2_str(start)} ~ {datetime_2_str(end)}]")

    return data


def generate_mock_load_bar_data(write_log_func: Callable = None):
    side_effect = mock.Mock(side_effect=partial(mock_load_bar_data, database_manager, write_log_func=write_log_func))
    return mock.patch.object(SqlManager, 'load_bar_data', side_effect)
