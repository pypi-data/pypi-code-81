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

from pytest import mark

from f4ratk.domain import Frequency, Region
from f4ratk.fama import ReturnsRequest


@mark.parametrize(
    'region, expected_source_ff, expected_source_mom',
    (
        (
            Region.DEVELOPED,
            'Developed_5_Factors_Daily',
            'Developed_Mom_Factor_Daily',
        ),
        (
            Region.DEVELOPED_EX_US,
            'Developed_ex_US_5_Factors_Daily',
            'Developed_ex_US_Mom_Factor_Daily',
        ),
        (
            Region.US,
            'F-F_Research_Data_5_Factors_2x3_daily',
            'F-F_Momentum_Factor_daily',
        ),
        (
            Region.EU,
            'Europe_5_Factors_Daily',
            'Europe_Mom_Factor_Daily',
        ),
    ),
)
def given_any_valid_region_and_daily_frequency_when_creating_request_should_map_to_remote_fama_data_set_names(  # noqa: E501
    region: Region,
    expected_source_ff: str,
    expected_source_mom: str,
):
    request = ReturnsRequest.of(region=region, frequency=Frequency.DAILY)

    assert request.frequency == Frequency.DAILY
    assert request.five.value == expected_source_ff
    assert request.momentum.value == expected_source_mom


@mark.parametrize(
    'region, expected_source_ff, expected_source_mom',
    (
        (
            Region.DEVELOPED,
            'Developed_5_Factors',
            'Developed_Mom_Factor',
        ),
        (
            Region.DEVELOPED_EX_US,
            'Developed_ex_US_5_Factors',
            'Developed_ex_US_Mom_Factor',
        ),
        (
            Region.US,
            'F-F_Research_Data_5_Factors_2x3',
            'F-F_Momentum_Factor',
        ),
        (
            Region.EU,
            'Europe_5_Factors',
            'Europe_Mom_Factor',
        ),
        (
            Region.EMERGING,
            'Emerging_5_Factors',
            'Emerging_MOM_Factor',
        ),
    ),
)
def given_any_valid_region_and_monthly_frequency_when_creating_request_should_map_to_remote_fama_data_set_names(  # noqa: E501
    region: Region,
    expected_source_ff: str,
    expected_source_mom: str,
):
    request = ReturnsRequest.of(region=region, frequency=Frequency.MONTHLY)

    assert request.frequency == Frequency.MONTHLY
    assert request.five.value == expected_source_ff
    assert request.momentum.value == expected_source_mom
