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

from unittest.mock import Mock

from numpy import dtype
from pandas import Period, PeriodDtype, PeriodIndex
from pandas.tseries.offsets import BusinessDay, MonthEnd
from pandas_datareader.famafrench import FamaFrenchReader
from pytest import mark, raises
from pytest_mock import MockerFixture

from f4ratk.domain import Frequency, Region
from f4ratk.fama import FamaReader
from f4ratk.shared import Normalizer
from tests.conftest import FamaFactory


class TestFamaReader:
    @mark.parametrize(
        'region',
        (region for region in Region),
    )
    def given_any_valid_region_and_monthly_frequency_should_return_data_with_monthly_period_index(  # noqa: E501
        self,
        region: Region,
    ):
        returns = FamaReader(None).fama_data(region=region, frequency=Frequency.MONTHLY)

        assert isinstance(returns.index, PeriodIndex)
        assert returns.index.dtype == PeriodDtype(freq=MonthEnd())

    @mark.parametrize(
        'region',
        (region for region in Region if region != Region.EMERGING),
    )
    def given_any_valid_region_and_daily_frequency_should_return_data_with_daily_period_index(  # noqa: E501
        self,
        region: Region,
    ):
        returns = FamaReader(Normalizer()).fama_data(
            region=region, frequency=Frequency.DAILY
        )

        assert isinstance(returns.index, PeriodIndex)
        assert returns.index.dtype == PeriodDtype(freq=BusinessDay())

    def given_emerging_region_for_daily_frequency_should_raise_value_error(self):
        with raises(ValueError):
            FamaReader(None).fama_data(
                region=Region.EMERGING, frequency=Frequency.DAILY
            )

    def given_any_region_for_any_frequency_should_return_five_factors_plus_momentum(
        self,
    ):
        returns = FamaReader(None).fama_data(
            region=Region.US, frequency=Frequency.MONTHLY
        )

        assert list(returns.columns) == ['MKT', 'SMB', 'HML', 'RMW', 'CMA', 'RF', 'WML']

    def given_data_missing_for_dates_when_reading_data_should_remove_missing_data(
        self, create_fama: FamaFactory, mocker: MockerFixture
    ):

        returns = create_fama(
            ('2020-04', -99.99),
            ('2020-05', -90.00),
            ('2020-06', -99.99),
        )

        reader_factory = mocker.patch('f4ratk.fama.fama_french_reader')

        fama_reader = Mock(spec_set=FamaFrenchReader)
        fama_reader.read.return_value = {0: returns}
        reader_factory.return_value = fama_reader

        result = FamaReader(normalizer=Normalizer()).fama_data(
            region=Region.EMERGING, frequency=Frequency.MONTHLY
        )

        assert len(result) == 1
        assert all([t is dtype(float) for t in result.dtypes])
        assert result.index[0] == Period('2020-05', 'M')
