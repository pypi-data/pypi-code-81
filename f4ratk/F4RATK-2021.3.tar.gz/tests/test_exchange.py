##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from datetime import date

from pandas import PeriodDtype, PeriodIndex
from pandas.tseries import offsets

from f4ratk.domain import Currency, Frequency
from f4ratk.exchange import ExchangeReader


def given_daily_frequency_when_reading_data_should_return_daily_exchange_rate():
    result = ExchangeReader(frequency=Frequency.DAILY).exchange_data(
        currency=Currency.EUR, start=date(2020, 9, 16), end=date(2020, 9, 16)
    )

    assert isinstance(result.index, PeriodIndex)
    assert result.index.dtype == PeriodDtype(freq=offsets.BusinessDay())

    assert result['Exchange Rate']['2020-09-16'] == 1.1835


def given_monthly_frequency_when_reading_data_should_return_monthly_exchange_rate():
    result = ExchangeReader(frequency=Frequency.MONTHLY).exchange_data(
        currency=Currency.EUR, start=date(2020, 9, 1), end=date(2020, 9, 30)
    )

    assert isinstance(result.index, PeriodIndex)
    assert result.index.dtype == PeriodDtype(freq=offsets.MonthEnd())

    assert len(result) == 1
    assert result['Exchange Rate']['2020-09'] == 1.1785


def should_rename_exchange_rate_column_to_generic_name():
    result = ExchangeReader(frequency=Frequency.DAILY).exchange_data(
        currency=Currency.EUR, start=date(2020, 9, 16), end=date(2020, 9, 16)
    )

    assert list(result.columns) == ['Exchange Rate']
