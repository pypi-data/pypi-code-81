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

from typing import Callable, Tuple, Union
from unittest.mock import Mock

from pandas import DataFrame, DatetimeIndex, PeriodIndex
from pandas_datareader.yahoo.daily import YahooDailyReader
from pytest import fixture
from pytest_mock import MockerFixture

from f4ratk.fama import FamaReader

Quote = Return = Tuple[str, float]
QuotesFactory = FamaFactory = ReturnsFactory = Callable[[Tuple[Return, ...]], DataFrame]

YahooReaderFactory = Callable[[Tuple[Quote, ...]], YahooDailyReader]
FamaReaderFactory = Callable[[Tuple[Return, ...]], FamaReader]


@fixture(scope='module', name="create_fama")
def fama_factory() -> FamaFactory:
    def _fama_factory(*returns: Return):
        periods, returns = list(zip(*returns))
        data = DataFrame(
            data={
                'MKT': returns,
                'SMB': returns,
                'HML': returns,
                'RMW': returns,
                'CMA': returns,
                'WML': returns,
                'RF': returns,
            },
            index=PeriodIndex(data=periods, dtype='period[M]'),
        )

        return data

    return _fama_factory


@fixture(scope='module', name="create_quotes")
def quotes_factory() -> QuotesFactory:
    def _quotes_factory(
        *quotes: Quote, index: Union[PeriodIndex, DatetimeIndex] = PeriodIndex
    ):
        index_data, returns = list(zip(*quotes))

        def create_index() -> Union[PeriodIndex, DatetimeIndex]:
            if index is PeriodIndex:
                return PeriodIndex(data=index_data, dtype='period[M]')
            elif index is DatetimeIndex:
                return DatetimeIndex(data=index_data, dtype='datetime64[ns]')

        data = DataFrame(
            data={'Adj Close': returns},
            index=create_index(),
        )

        return data

    return _quotes_factory


@fixture(scope='module', name="create_returns")
def returns_factory() -> ReturnsFactory:
    def _returns_factory(
        *quotes: Quote, index: Union[PeriodIndex, DatetimeIndex] = PeriodIndex
    ):
        index_data, returns = list(zip(*quotes))

        def create_index() -> Union[PeriodIndex, DatetimeIndex]:
            if index is PeriodIndex:
                return PeriodIndex(data=index_data, dtype='period[M]')
            elif index is DatetimeIndex:
                return DatetimeIndex(data=index_data, dtype='datetime64[ns]')

        data = DataFrame(
            data={'Returns': returns},
            index=create_index(),
        )

        return data

    return _returns_factory


@fixture(scope='function', name="yahoo_returns")
def yahoo_reader_factory(
    mocker: MockerFixture, create_quotes: QuotesFactory
) -> YahooReaderFactory:
    def _yahoo_reader_factory(*quotes: Quote):
        mock_reader = Mock()
        mock_reader.read.return_value = create_quotes(
            *quotes,
            index=DatetimeIndex,
        )
        mocker.patch(
            'f4ratk.ticker.reader.yahoo_reader',
            spec_set=YahooDailyReader,
            return_value=mock_reader,
        )

    return _yahoo_reader_factory


@fixture(scope='function', name="fama_returns")
def fama_reader_factory(
    mocker: MockerFixture, create_fama: FamaFactory
) -> FamaReaderFactory:
    def _fama_reader_factory(*returns: Return):
        returns = create_fama(*returns)
        mocker.patch(
            'f4ratk.infrastructure.FamaReader',
            spec_set=FamaReader,
            **{'fama_data.return_value': returns},
        )

    return _fama_reader_factory
