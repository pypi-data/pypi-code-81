# @author: slowchen
# @email: 644209001@qq.com
# @file: core.py
# @date: 2021/04/12
# @site: https://buggg.orgjuices.com/
from datetime import datetime, date

import arrow


class DayCalculator:
    """
    获取本月区间，当前日期为26日前，则为上月25-本月26
    当前日期在26日后，则为本月26-下月25
    当前日期为26，则为26日
    :param time:
    :return:
    start: 本月开始日期
    end: 本月结束日期
    pre_start: 上月开始日期
    pre_end: 上月结束日期
    yesterday: 本月前一天日期
    pre_yesterday: 上月前一天日期
    days: 本月开始日期至前一天日期的总天数
    """

    def __init__(self, default_start_date=1, time: arrow.Arrow = arrow.now()):
        self.start_date = default_start_date
        self.time = time
        self.year = self.time.year
        self.month = self.time.month
        self.day = self.time.day
        if default_start_date == 1:
            self._default()
        else:
            self._prepare()

    def _default(self):
        self._start = arrow.get(date(self.year, self.month, 1))
        self._pre_start = self._start.shift(months=-1)
        self._end = arrow.get(date(self.year, self.month + 1, 1)).shift(days=-1)
        self._pre_end = self._start.shift(days=-1)
        self._yesterday = self.time.shift(days=-1)
        self._pre_yesterday = self._yesterday.shift(months=-1)
        self._days = (self.time - self._start).days

    def _prepare(self):
        if self.day == self.start_date:
            # 当前日期为26，则为26日
            self._start = arrow.get(date(self.year, self.month, self.start_date))
            self._end = arrow.get(date(self.year, self.month, self.start_date))
            self._yesterday = self._end
            self._days = 1
        elif self.day < self.start_date:
            # 当前日期为26日前，则为上月25 - 本月26
            pre_month_time = self.time.shift(months=-1)
            start_year = pre_month_time.year
            start_month = pre_month_time.month
            self._start = arrow.get(date(start_year, start_month, self.start_date))
            end_year = self.year
            end_month = self.month
            self._end = arrow.get(date(end_year, end_month, self.start_date - 1))

            pre_date_time = self.time.shift(days=-1)
            self._yesterday = arrow.get(
                date(pre_date_time.year, pre_date_time.month, pre_date_time.day))

            self._days = (self._yesterday - self._start).days + 1

        else:
            # 当前日期在26日后，则为本月26-下月25
            self._start = arrow.get(date(self.year, self.month, self.start_date))
            next_month_time = self.time.shift(months=1)
            end_year = next_month_time.year
            end_month = next_month_time.month
            self._end = arrow.get(date(end_year, end_month, self.start_date - 1))
            pre_date_time = self.time.shift(days=-1)
            self._yesterday = arrow.get(
                date(pre_date_time.year, pre_date_time.month, pre_date_time.day))

            self._days = (self._yesterday - self._start).days + 1

        self._pre_yesterday = self._yesterday.shift(months=-1)
        self._pre_start = self._start.shift(months=-1)
        self._pre_end = self._end.shift(months=-1)

    def get_pre_month(self):
        """
        获取上月日期
        :return:2021-01-01
        """
        if self.day < 26:
            pre_month_date = self.time.shift(months=-1)
            pre_month = arrow.get(date(pre_month_date.year, pre_month_date.month, 1))
            # pre_month = f'{pre_month_date.year}-{pre_month_date.month}-01'
        else:
            # pre_month = f'{time.year}-{time.month}-01'
            pre_month = arrow.get(date(self.year, self.month, 1))
        return pre_month

    def get_pre_month_1(self):
        """
        获取上上月日期
        :return:2020-12-01
        """
        return self.get_pre_month().shift(months=-1)

    @property
    def pre_month(self):
        return self.get_pre_month().date()

    @property
    def pre_month_1(self):
        return self.get_pre_month_1().date()

    @property
    def start(self):
        return self._start.date()

    @property
    def end(self):
        return self._end.date()

    @property
    def pre_start(self):
        return self._pre_start.date()

    @property
    def pre_start_1(self):
        return self._pre_start.shift(months=-1).date()

    @property
    def pre_end(self):
        return self._pre_end.date()

    @property
    def pre_end_1(self):
        return self._pre_end.shift(months=-1).date()

    @property
    def yesterday(self):
        return self._yesterday.date()

    @property
    def pre_yesterday(self):
        return self._pre_yesterday.date()

    @property
    def days(self):
        return self._days

    @property
    def today_start(self):
        return self.get_today_start().format()

    @property
    def today_end(self):
        return self.get_today_end().format()

    @property
    def pre_today_start(self):
        return self.get_today_start().shift(months=-1).format()

    @property
    def pre_today_end(self):
        return self.get_today_end().shift(months=-1).format()

    @property
    def pre_week_date(self):
        return self.time.shift(weeks=-1).date()

    def get_today_start(self):
        """
        获取今日开始时间，例如当前2021-01-13 15:51:30,则返回2021-01-13 00:00:00
        :return:
        """
        return arrow.get(datetime(self.year, self.month, self.day, 0, 0, 0))

    def get_today_end(self):
        """
        获取今日截止到当前小时数的时间，例如当前2021-01-13 15:51:30,则返回2021-01-13 15:00:00
        :return:
        """
        return arrow.get(datetime(self.year, self.month, self.day, self.time.hour, 0, 0))


if __name__ == '__main__':
    a = DayCalculator(default_start_date=2)
    print(a.pre_week_date)
