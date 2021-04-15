"""Tests for the OHLCV class."""
# pylint: disable=W9015,W9016

from unittest import mock

import pytest

from trading.etl.ohlcv.core import errors
from trading.etl.ohlcv.core.metadata import Timeframe
from trading.etl.ohlcv.core.ohlcv import OHLCV


@pytest.fixture(name='ohlcv', scope="class")
def fixture_ohlcv():
    """Initialized OHLCV instance fixture."""
    ohlcv = OHLCV([
        # 'BTC/BUSD', '1h', 1609430400000, limit=5
        [1609430400000, 28797.33, 28844.28, 28322.89, 28403.27, 781.18027],
        [1609434000000, 28399.64, 28743.62, 28373.21, 28593.17, 750.537798],
        [1609437600000, 28592.12, 28922.78, 28503.93, 28896.91, 754.077604],
        [1609441200000, 28896.83, 29036.99, 28770.48, 28933.01, 766.929273],
        [1609444800000, 28933.01, 29177.48, 28905.92, 29160.83, 409.665109],
    ])
    ohlcv.metadata.exchange = 'Binance'
    ohlcv.metadata.symbol = 'BTC/BUSD'

    return ohlcv


class TestOHLCV:
    """Test class for the OHLCV class."""

    def test_correct_instance(self, ohlcv):
        assert isinstance(ohlcv, OHLCV)
        assert isinstance(ohlcv[:-1], OHLCV)

    def test_successful_timeframe_detection(self, ohlcv):
        assert ohlcv.timeframe == '1h'

    def test_unsuccessful_timeframe_detection(self):
        """Check automated timeframe detection in OHLCV class."""
        ohlcv = OHLCV([])
        assert ohlcv.timeframe.interval is None
        assert ohlcv.timeframe.unit is None

        ohlcv = OHLCV([
            # Random data
            [1609430400000, 28797.33, 28844.28, 28322.89, 28403.27, 781.18027],
            [1609434510002, 28399.64, 28743.62, 28373.21, 28593.17, 750.53798],
        ])
        assert ohlcv.timeframe.interval is None
        assert ohlcv.timeframe.unit is None

    def test_metadata_is_valid(self, ohlcv):
        assert ohlcv.metadata
        assert ohlcv.metadata.exchange == 'Binance'
        assert ohlcv.metadata.symbol == 'BTC/BUSD'

    def test_timeframe_is_valid(self, ohlcv):
        assert ohlcv.timeframe
        assert isinstance(ohlcv.timeframe, Timeframe)
        assert ohlcv.timeframe.interval == 1.0
        assert ohlcv.timeframe.unit == 'h'

    def test_timeframe_is_invalid(self, ohlcv):
        with pytest.raises(errors.InvalidTimeframeError):
            ohlcv.timeframe = ['an', 'invalid', 'timeframe']

    def test_successful_generate_db_query(self, ohlcv):
        """Test the generation of DB Query given a valid OHLCV."""
        expected_query = "INSERT INTO ohlcv_1h (market_id, opening_timestamp, "
        expected_query += "opening_price, highest_price, lowest_price, "
        expected_query += "closing_price, trading_volume) VALUES (1877,"
        expected_query += "'2020-12-31 16:00:00',28797.33,28844.28,28322.89,"
        expected_query += "28403.27,781.18027),(1877,'2020-12-31 17:00:00'"
        expected_query += ",28399.64,28743.62,28373.21,28593.17,750.537798)"
        expected_query += ",(1877,'2020-12-31 18:00:00',28592.12,28922.78"
        expected_query += ",28503.93,28896.91,754.077604),(1877,'2020-12-31 "
        expected_query += "19:00:00',28896.83,29036.99,28770.48,28933.01,"
        expected_query += "766.929273),(1877,'2020-12-31 20:00:00',28933.01,"
        expected_query += "29177.48,28905.92,29160.83,409.665109)"

        assert ohlcv.generate_db_query() == expected_query

    def test_generate_db_query_with_missing_metadata(self):
        empty_ohlcv = OHLCV([])
        with pytest.raises(errors.DBQueryGenerationError):
            empty_ohlcv.generate_db_query()

    @mock.patch("psycopg2.connect", mock.MagicMock(return_value="None"))
    def test_generate_db_query_failed_db_connection(self, ohlcv):
        with pytest.raises(errors.DBQueryGenerationError):
            ohlcv.generate_db_query()

    def test_generate_db_query_non_existent_exchange(self):
        """Test the generation of DB Query given an invalid OHLCV metadata."""
        non_existent_ohlcv = OHLCV([
            # 'BTC/BUSD', '1h', 1609430400000, limit=5
            [1609430400000, 28797.33, 28844.28, 28322.89, 28403.27, 781.18027],
            [1609434000000, 28399.64, 28743.62, 28373.21, 28593.17, 750.53779],
            [1609437600000, 28592.12, 28922.78, 28503.93, 28896.91, 754.07760],
        ])
        non_existent_ohlcv.metadata.exchange = 'Testeroo'
        non_existent_ohlcv.metadata.symbol = 'TEST/TEST'

        with pytest.raises(errors.DBQueryGenerationError):
            non_existent_ohlcv.generate_db_query()
