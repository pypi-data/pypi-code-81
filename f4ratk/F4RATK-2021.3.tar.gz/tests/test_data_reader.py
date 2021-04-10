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

from datetime import date, timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable

from numpy import dtype

from f4ratk.data_reader import (
    CsvFileReader,
    fama_french_reader,
    fred_reader,
    yahoo_reader,
)


class TestFamaReader:
    def should_create_fama_reader_for_given_returns_data_name(self):
        result = fama_french_reader(returns_data='Developed_5_Factors_Daily')
        assert result.symbols == 'Developed_5_Factors_Daily'

    def should_create_fama_reader_with_cache(self):
        result = fama_french_reader(returns_data='')

        assert result.session.expire_after == timedelta(days=14)
        assert result.session._cache_name.endswith('requests')

    def should_query_full_data_range_by_default(self):
        result = fama_french_reader(returns_data='')

        assert result.start == date(1920, 1, 1)


class TestYahooReader:
    def should_create_yahoo_reader_for_given_ticker_symbol_and_date_range(self):
        result = yahoo_reader(
            ticker_symbol="V6IC.DE", start=date(2014, 1, 1), end=date(2019, 12, 31)
        )
        assert result.symbols == 'V6IC.DE'
        assert result.start == date(2014, 1, 1)
        assert result.end == date(2019, 12, 31)

    def should_create_yahoo_reader_with_cache(self):
        result = yahoo_reader(ticker_symbol=None, start=None, end=None)

        assert result.session.expire_after == timedelta(days=14)
        assert result.session._cache_name.endswith('requests')

    def should_query_full_data_range_by_default(self):
        result = yahoo_reader(ticker_symbol=None, start=None, end=None)

        assert result.start == date(1970, 1, 1)


class TestFredReader:
    def should_create_fred_reader_for_given_exchange_symbol_and_date_range(self):
        result = fred_reader(
            exchange_symbol='DEXUSEU', start=date(2014, 1, 1), end=date(2019, 12, 31)
        )
        assert result.symbols == 'DEXUSEU'
        assert result.start == date(2014, 1, 1)
        assert result.end == date(2019, 12, 31)

    def should_create_fred_reader_with_cache(self):
        result = fred_reader(exchange_symbol=None, start=None, end=None)

        assert result.session.expire_after == timedelta(days=14)
        assert result.session._cache_name.endswith('requests')

    def should_query_full_data_range_by_default(self):
        result = fred_reader(exchange_symbol=None, start=None, end=None)

        assert result.start == date(1970, 1, 1)


class TestCsvFileReader:
    def when_read_file_with_content(self, lines: Iterable[str]):
        pass

    def should_parse_isodate_and_returns_column(self):
        with NamedTemporaryFile(mode='w+', prefix='f4ratk_test_tmp_') as file:
            print(
                *('2020-11-18,"15.35"', '2020-11-17,14.33'),
                sep='\n',
                end='\n',
                file=file
            )

            file.flush()

            result = CsvFileReader(path=Path(file.name)).read()

        assert len(result) == 2
        assert result.index.dtype == dtype('datetime64[ns]')
        assert result.index.name == 'Dates'
        assert list(result.columns) == ['Returns']

        assert result['Returns']['2020-11-18'][0] == 15.35
        assert result['Returns']['2020-11-17'][0] == 14.33
