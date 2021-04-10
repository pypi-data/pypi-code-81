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

from pandas import Period
from pytest import approx

from f4ratk.domain import Frequency, Region
from f4ratk.fama import FamaReader
from f4ratk.history import Historian
from tests.conftest import FamaFactory


class TestAnnualizedReturns:
    def given_factor_returns_when_displaying_history_for_region_should_calc_annualized_returns_from_monthly_fama_data(  # noqa: E501
        self, create_fama: FamaFactory
    ):
        returns = create_fama(
            ('2020-04', -5.0),
            ('2020-05', 10.0),
            ('2020-06', -5.0),
            ('2020-07', 10.0),
            ('2020-08', -5.0),
            ('2020-09', 10.0),
            ('2020-10', -5.0),
            ('2020-11', 10.0),
            ('2020-12', -5.0),
            ('2021-01', 10.0),
            ('2021-02', -5.0),
            ('2021-03', 10.0),
            ('2021-04', -5.0),
        )

        fama_reader = Mock(spec_set=FamaReader)
        fama_reader.fama_data.return_value = returns

        result = Historian(fama_reader).annualized_returns(region=Region.US)

        assert list(result._data.columns) == ['Returns', 'SD']
        assert result._data['Returns']['MKT'] == approx(21.706, rel=0.0001)
        assert result._data['SD']['MKT'] == approx(26.961, rel=0.0001)

        assert result._first == Period('2020-04', 'M')
        assert result._last == Period('2021-04', 'M')

        fama_reader.fama_data.assert_called_once_with(
            region=Region.US, frequency=Frequency.MONTHLY
        )
