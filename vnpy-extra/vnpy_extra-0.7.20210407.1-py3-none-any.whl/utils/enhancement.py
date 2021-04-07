"""
@author  : MG
@Time    : 2020/10/9 13:49
@File    : enhancement.py
@contact : mmmaaaggg@163.com
@desc    : 用于对 vnpy 内置的各种类及函数进行增强
"""
import collections
import inspect
import re
from datetime import timedelta, time
from enum import Enum
from typing import Callable, Union, Tuple, Optional

import numpy as np
import pandas as pd
import talib
from vnpy.app.cta_strategy import (
    BarData,
    BarGenerator as BarGeneratorBase,
    ArrayManager as ArrayManagerBase,
    CtaSignal as CtaSignalBase,
)
from vnpy.trader.constant import Interval
from vnpy.trader.object import TickData

from vnpy_extra.config import logging
from vnpy_extra.constants import INSTRUMENT_TRADE_TIME_PAIR_DIC

logger = logging.getLogger()
pattern4 = re.compile(r"(?<=\D)\d{4}")
pattern2 = re.compile(r"(?<=\D)\d{2}")
PATTERN_INSTRUMENT_TYPE = re.compile(r'\D+(?=\d{2,4})', re.IGNORECASE)
PATTERN_INSTRUMENT_TYPE_RESTRICT = re.compile(r'\D+(?=\d{2,4}$)', re.IGNORECASE)
PATTERN_INSTRUMENT_TYPE_EXCHANGE_SPLIT = re.compile(r"(?<=\D)\d{3,4}\.", re.IGNORECASE)


class PriceTypeEnum(Enum):
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'


def get_contract_month(contract: str):
    """
    根据合约名称获取合约的月份，包括月份连续合约的格式，例如。RB01.SHF
    """
    match = pattern4.search(contract)
    if match is not None:
        return int(match.group()[2:])
    match = pattern2.search(contract)
    if match is not None:
        return int(match.group())
    raise ValueError(f'合约 {contract} 格式无效')


def get_instrument_type(symbol, pattern=None):
    """匹配 instrument_type"""
    if pattern is None:
        pattern = PATTERN_INSTRUMENT_TYPE

    match = pattern.search(symbol)
    if match is not None:
        instrument_type = match.group()
    else:
        logger.error("当前合约 %s 无法判断期货品种", symbol)
        instrument_type = None

    return instrument_type.upper() if instrument_type is not None else None


def get_instrument_type_and_exchange(vt_symbol, pattern=None):
    if pattern is None:
        pattern = PATTERN_INSTRUMENT_TYPE_EXCHANGE_SPLIT
    ret = pattern.split(vt_symbol)
    assert len(ret) == 2, f'{vt_symbol} 无法被识别'
    return ret


def _test_get_instrument_type_and_exchange():
    ret = get_instrument_type_and_exchange('rb9999.shfe')
    assert ret == ['rb', 'shfe']
    try:
        ret = get_instrument_type_and_exchange('9999.shfe')
        assert False, '不应该被识别'
    except AssertionError:
        pass


def change_main_contract(vt_symbol) -> str:
    """将某一个合约品种变为主力连续合约"""
    new_vt_symbol = get_instrument_type(vt_symbol) + '9999.' + vt_symbol.split('.')[-1]
    return new_vt_symbol


class BarGenerator(BarGeneratorBase):
    def __init__(
            self,
            on_bar: Callable,
            window: int = 0,
            on_window_bar: Callable = None,
            interval: Interval = Interval.MINUTE,
            strict=False
    ):
        super().__init__(on_bar, window, on_window_bar, interval)
        self.instrument_type = None
        self.trade_end_time = None
        # 记录上一个触发 self.on_window_bar 的 bar 实例
        self.last_finished_bar = None
        # 记录 1m bar的数量
        self.bar_count = 0
        # 记录上一次生产 window_bar 时，对应的 bar_count
        self._last_finished_bar_no = 0
        self.strict = strict
        # 记录上一次 (bar.datetime.minute + 1) % self.window 的余数结果
        self._last_mod_remainder = 0

    def is_trade_end(self, bar):
        is_end = bar.datetime.time() == self.trade_end_time
        return is_end

    def is_end_day(self, bar):
        if self.is_trade_end(bar):
            is_end = True
        else:
            # 有些情况下，当前最后一个时段bar没有，这种情况下只能通过下一个交易日的bar与当前bar日期是否一致来判断
            # 防止夜盘数据触发跨日，5点以后才做检查
            # bar 的日期与 self.window_bar 日期不一致时，说明已经跨天了
            is_end = bar.datetime.hour > 5 \
                     and bar.datetime.date() != self.window_bar.datetime.date()

        return is_end

    def is_end_week(self, bar):
        """判断但却bar是否是周末最后一根"""
        # isocalendar()[:2] 匹配年号和周数
        if self.is_trade_end(bar):
            # 判断当日是否是收盘时间，且即将跨周(周五+2天为周日，跨周）
            # 该逻辑不够严谨，对于周一跨周的计算机需要+3，这里暂不考虑

            is_end = (bar.datetime + timedelta(days=2)).isocalendar()[:2] != self.last_bar.datetime.isocalendar()[:2]
        else:
            # 有些情况下，当前最后一个时段bar没有，这种情况下只能通过下一个交易日的bar与当前bar周数是否一致来判断
            is_end = bar.datetime.isocalendar()[:2] != self.last_bar.datetime.isocalendar()[:2]

        return is_end

    def update_bar(self, bar: BarData) -> None:
        """
        Update 1 minute bar into generator
        """
        self.bar_count += 1
        if self.instrument_type is None:
            self.instrument_type = get_instrument_type(bar.symbol)
            if self.instrument_type in INSTRUMENT_TRADE_TIME_PAIR_DIC:
                self.trade_end_time = INSTRUMENT_TRADE_TIME_PAIR_DIC[self.instrument_type][1]
            else:
                logger.error("当前合约 %s 对应品种 %s 没有对应的交易时段，默认15点收盘",
                             bar.symbol, self.instrument_type)
                self.trade_end_time = time(15, 0, 0)

        # If not inited, create window bar object
        if not self.window_bar:
            # Generate timestamp for bar data
            if self.interval == Interval.MINUTE:
                dt = bar.datetime.replace(second=0, microsecond=0)
            else:
                dt = bar.datetime.replace(minute=0, second=0, microsecond=0)

            self.window_bar = BarData(
                symbol=bar.symbol,
                exchange=bar.exchange,
                datetime=dt,
                gateway_name=bar.gateway_name,
                open_price=bar.open_price,
                high_price=bar.high_price,
                low_price=bar.low_price
            )
        # Otherwise, update high/low price into window bar
        else:
            self.window_bar.high_price = max(
                self.window_bar.high_price, bar.high_price)
            self.window_bar.low_price = min(
                self.window_bar.low_price, bar.low_price)

        # Update close price/volume into window bar
        self.window_bar.close_price = bar.close_price
        self.window_bar.volume += int(bar.volume)
        self.window_bar.open_interest = bar.open_interest

        # Check if window bar completed
        finished = False

        if self.interval == Interval.MINUTE:
            # x-minute bar
            if self.strict:
                remainder = (bar.datetime.minute + 1) % self.window
                if remainder == 0 or remainder < self._last_mod_remainder:
                    # remainder < self._last_mod_remainder 说明跨时间段情况出现。
                    # 例如：30分钟周期情况下 10:15 交易所进入休息时段，下一次开盘时间10:30。
                    # 用 (bar.datetime.minute + 1) % self.window 的逻辑将错过此次bar生成。
                    # 而在当前逻辑下，将会在10:30分时生成一个 10:00 ~ 10:15时段的 bar 最为 30m bar
                    finished = True

                self._last_mod_remainder = remainder
            elif not (bar.datetime.minute + 1) % self.window:
                finished = True

        elif self.interval == Interval.HOUR:
            if self.last_bar:
                new_hour = self.last_finished_bar != self.last_bar and bar.datetime.hour != self.last_bar.datetime.hour
                last_minute = bar.datetime.minute == 59

                if new_hour or last_minute:
                    # 1-hour bar
                    if self.window == 1:
                        finished = True
                    # x-hour bar
                    else:
                        self.interval_count += 1

                        if not self.interval_count % self.window:
                            finished = True
                            self.interval_count = 0

        elif self.interval == Interval.DAILY:
            if self.last_bar and self.last_finished_bar != self.last_bar and self.is_end_day(bar):
                # 1-day bar
                if self.window == 1:
                    finished = True
                # x-day bar
                else:
                    self.interval_count += 1

                    if not self.interval_count % self.window:
                        finished = True
                        self.interval_count = 0
        elif self.interval == Interval.WEEKLY:
            if self.last_bar and self.last_finished_bar != self.last_bar and self.is_end_week(bar):
                # 1-day bar
                if self.window == 1:
                    finished = True
                # x-day bar
                else:
                    self.interval_count += 1

                    if not self.interval_count % self.window:
                        finished = True
                        self.interval_count = 0

        # 判断是否当前 bar 结束
        if finished:
            self.on_window_bar(self.window_bar)
            self.last_finished_bar = bar
            self._last_finished_bar_no = self.bar_count
            self.window_bar = None

        # Cache last bar object
        self.last_bar = bar


class ArrayManager(ArrayManagerBase):

    def __init__(self, size: int = 100, base_price_type=PriceTypeEnum.close):
        """
        行情数组
        :param size:数组尺寸
        :param base_price_type:（默认为close）。数组的基础价格类型。对于单一指标而言，计算RSI、MACD等指标时使用的默认价格类型，
        """
        super().__init__(size=size)
        # 用于记录每一个 MACD， KDJ，RSI等每一个指标最近一次被调用时候的 count 值。
        # 该值主要是用来在进行指数标准化(z-score)时为了防止重复训练而记录的一个标识位，
        # 每一次新的训练都从该标识位开始往后进行训练，这样以便保证么一次训练均是最新数据
        # 默认情况下 指标都是0上下浮动或者0~1之间浮动，因此，不做均值处理，只除以方差，避免出现0轴偏移的情况
        from sklearn.preprocessing import StandardScaler
        self.index_last_invoked_count_dic = collections.defaultdict(lambda: (0, StandardScaler(with_mean=False)))
        self.fit_threshold = int(self.size * 0.9)  # 超过90% 再进行 fit
        self.base_price_type = base_price_type \
            if isinstance(base_price_type, PriceTypeEnum) else PriceTypeEnum[base_price_type]
        if base_price_type == PriceTypeEnum.close:
            self.base_price = self.close
        elif base_price_type == PriceTypeEnum.open:
            self.base_price = self.open
        elif base_price_type == PriceTypeEnum.high:
            self.base_price = self.high
        elif base_price_type == PriceTypeEnum.low:
            self.base_price = self.low
        else:
            raise ValueError(f"base_price_type={base_price_type} 无效")

    def kdj(self, fastk_period: int, slowk_period: int, slowd_period: int, array: bool = False):
        # KDJ 值对应的函数是 STOCH
        slowk, slowd = talib.STOCH(
            self.high, self.low, self.close,
            fastk_period=fastk_period,
            slowk_period=slowk_period,
            slowk_matype=0,
            slowd_period=slowd_period,
            slowd_matype=0)
        # 求出J值，J = (3*K)-(2*D)
        slowj = list(map(lambda x, y: 3 * x - 2 * y, slowk, slowd))
        if array:
            return slowk, slowd, slowj
        return slowk[-1], slowd[-1], slowj[-1]

    def rsi(self, n: int, array: bool = False) -> Union[float, np.ndarray]:
        """
        Relative Strenght Index (RSI).
        """
        result = talib.RSI(self.base_price, n)
        if array:
            return result
        return result[-1]

    def ma(self, *args, price=None, matype=0, array: bool = False):
        """
        ta.MA(close,timeperiod=30,matype=0)
        移动平均线系列指标包括：SMA简单移动平均线、EMA指数移动平均线、WMA加权移动平均线、DEMA双移动平均线、TEMA三重指数移动平均线、TRIMA三角移动平均线、KAMA考夫曼自适应移动平均线、MAMA为MESA自适应移动平均线、T3三重指数移动平均线。
        其中，close为收盘价，时间序列，timeperiod为时间短，默认30天，
        :param args:
        :param price: 价格序列，默认为None，使用 self.base_price 作为计算基准
        :param matype: matype 分别对应：0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        :param array: 是否返回数组
        :return:
        """
        if price is None:
            price = self.base_price

        rets = [talib.MA(price, win, matype) for win in args]

        if array:
            return tuple(rets)

        return tuple([_[-1] for _ in rets])

    def record_index_used(self, model, func_name=None):
        """记录该指标的索引值"""
        if func_name is None:
            func_name = inspect.stack()[1][3]
        self.index_last_invoked_count_dic[func_name] = (self.count, model)
        return func_name, self.count

    def get_index_last_used(self, func_name=None):
        """
        获取该指标的索引值
        """
        if func_name is None:
            func_name = inspect.stack()[1][3]
        return func_name, self.index_last_invoked_count_dic[func_name]

    def macd(
            self,
            fast_period: int,
            slow_period: int,
            signal_period: int,
            z_score: bool = False,
            array: bool = False,
    ) -> Union[
        Tuple[np.ndarray, np.ndarray, np.ndarray],
        Tuple[float, float, float]
    ]:
        """
        MACD.
        """
        macd, signal, hist = talib.MACD(
            self.base_price, fast_period, slow_period, signal_period
        )
        if z_score:
            func_name = 'macd'
            _, (count_last, model) = self.get_index_last_used(func_name)
            # 计算需要进行训练的数量
            count_fit = self.count - count_last
            if self.fit_threshold < count_fit:
                if count_last == 0:
                    # 首次训练
                    x = np.concatenate([
                        macd[-count_fit:][:, np.newaxis],
                        signal[-count_fit:][:, np.newaxis],
                        hist[-count_fit:][:, np.newaxis],
                    ], axis=1)
                    x = model.fit_transform(x)
                elif count_fit > self.size:
                    # 全数据增量训练
                    x = np.concatenate([
                        macd[:, np.newaxis],
                        signal[:, np.newaxis],
                        hist[:, np.newaxis],
                    ], axis=1)
                    x = model.partial_fit(x)
                else:
                    # 部分数据增量训练
                    x = np.concatenate([
                        macd[-count_fit:][:, np.newaxis],
                        signal[-count_fit:][:, np.newaxis],
                        hist[-count_fit:][:, np.newaxis],
                    ], axis=1)
                    model.partial_fit(x)
                    x = np.concatenate([
                        macd[:, np.newaxis],
                        signal[:, np.newaxis],
                        hist[:, np.newaxis],
                    ], axis=1)
                    x = model.transform(x)

                # 记录当前指数被使用时的 Count
                self.record_index_used(model, func_name)
            else:
                # 全数据转换
                x = np.concatenate([
                    macd[:, np.newaxis],
                    signal[:, np.newaxis],
                    hist[:, np.newaxis],
                ], axis=1)
                x = model.transform(x)

            # 恢复成 指标
            macd = x[:, 0]
            signal = x[:, 1]
            hist = x[:, 2]

        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]


def generate_available_period(contract_month: int, date_from_str: str, date_to_str: str) -> list:
    """
    生成合约对应的有效日期范围，与给点日期范围的交集
    该功能仅用于策略回测是对1月份连续合约等连续合约数据是使用
    根据合约生成日期范围规则，例如：
    1月合约，上一年8月1 ~ 11月31日
    5月合约，上一年12月1 ~ 3月31日
    9月合约，4月1日 ~ 7月31日
    """
    date_from = pd.to_datetime(date_from_str if date_from_str is not None else '2000-01-01')
    date_to = pd.to_datetime(date_to_str if date_from_str is not None else '2030-01-01')
    periods = []
    for range_year in range(date_from.year, date_to.year + 2):
        year, month = (range_year, contract_month - 5) if contract_month > 5 else (
            range_year - 1, contract_month + 12 - 5)
        range_from = pd.to_datetime(f"{year:4d}-{month:02d}-01")
        year, month = (range_year, contract_month - 1) if contract_month > 1 else (
            range_year - 1, 12)
        range_to = pd.to_datetime(f"{year:4d}-{month:02d}-01") - pd.to_timedelta(1, unit='D')
        # 与 date_from date_to 取交集
        if range_to < date_from or date_to < range_from:
            continue
        range_from = date_from if range_from < date_from < range_to else range_from
        range_to = date_to if range_from < date_to < range_to else range_to
        periods.append([str(range_from.date()), str(range_to.date())])

    return periods


class CtaSignal(CtaSignalBase):

    def __init__(self, period: int, array_size: int, interval: Interval = Interval.MINUTE, filter_n_available=1,
                 strict=False, base_price_type=PriceTypeEnum.close):
        """

        :param period 周期数
        :param array_size 行情队列大小
        :param interval 周期类型
        :param filter_n_available 有效信号过滤器,超过指定次数后才真正改变 signal_pos 信号数值
        :param strict 是否使用 strict 模式生成 window bar
        """
        super().__init__()
        self.period = period
        self.interval = interval
        self.bg = BarGenerator(
            on_bar=self.on_bar, window=self.period, on_window_bar=self.on_window, interval=self.interval,
            strict=strict)
        self.am = ArrayManager(size=array_size, base_price_type=base_price_type)
        self.bar: Optional[BarData] = None
        self.win_bar: Optional[BarData] = None
        self.win_bar_count = 0
        self.filter_n_available = filter_n_available
        self._n_available_counter = 0
        self._n_available_pos = self.signal_pos

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bar = bar
        self.bg.update_bar(bar)

    def on_window(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        self.win_bar = bar
        self.win_bar_count += 1

    def set_signal_pos(self, pos):
        """对 set_signal_pos 增加过滤器,重复超过 self.filter_n_available 次时才算有效"""
        if pos != self._n_available_pos:
            self._n_available_pos = pos
            self._n_available_counter = 1
        else:
            self._n_available_counter += 1

        if self._n_available_counter >= self.filter_n_available:
            super().set_signal_pos(pos)


if __name__ == "__main__":
    _test_get_instrument_type_and_exchange()
