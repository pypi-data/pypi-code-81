"""Tests for the OHLCV metadata classes."""

import pytest

from trading.etl.ohlcv.core.metadata import OHLCVMetadata
from trading.etl.ohlcv.core.metadata import Timeframe
from trading.etl.ohlcv.core import errors


@pytest.fixture(name='metadata', scope="class")
def fixture_metadata():
    metadata = OHLCVMetadata()
    metadata.exchange = 'Bitmex'
    metadata.symbol = 'BTCUSDT'

    return metadata


@pytest.fixture(name='timeframe', scope="class")
def fixture_timeframe():
    return Timeframe('3d')


class TestMetadata:
    """Test class for the OHLCVMetadata class."""

    def test_correct_instance(self, metadata):
        assert isinstance(metadata, OHLCVMetadata)

    def test_exchange_is_valid(self, metadata):
        assert metadata.exchange
        assert isinstance(metadata.exchange, str)
        assert metadata.exchange == 'Bitmex'

    def test_symbol_is_valid(self, metadata):
        assert metadata.symbol
        assert isinstance(metadata.symbol, str)
        assert metadata.symbol == 'BTCUSDT'

    def test_repr_function(self, metadata):
        assert repr(metadata).startswith(f'{OHLCVMetadata.__name__}(')
        assert repr(metadata).endswith(')')

        assert f'exchange={metadata.exchange!r}' in repr(metadata)
        assert f'symbol={metadata.symbol!r}' in repr(metadata)
        assert ',' in repr(metadata)


class TestTimeframe:
    """Test class for the Timeframe class."""

    def test_correct_instance(self, timeframe):
        assert isinstance(timeframe, Timeframe)

    def test_other_initializations(self):
        """Tests for other init cases that's not covered by fixture."""
        timeframe = Timeframe(interval='8', unit='h')
        assert timeframe.interval == 8
        assert timeframe.unit == 'h'

        timeframe = Timeframe(timeframe)
        assert timeframe.interval == 8
        assert timeframe.unit == 'h'

        timeframe = Timeframe()
        assert timeframe.interval is None
        assert timeframe.unit is None

    def test_invalid_initialization(self):
        with pytest.raises(errors.InvalidTimeframeError):
            Timeframe(interval=['invalid', 'interval'], unit='h')

    def test_interval_is_valid(self, timeframe):
        assert timeframe.interval
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == 3

    def test_timeframe_unit_is_valid(self, timeframe):
        assert timeframe.unit
        assert isinstance(timeframe.unit, str)
        assert timeframe.unit == 'd'

    def test_timeframe_unit_is_invalid(self, timeframe):
        with pytest.raises(errors.UnknownTimeframeUnitError):
            timeframe.unit = 'some unknown unit'

    def test_get_duration_unit_is_valid(self, timeframe):
        assert pytest.approx(timeframe.get_duration('y')) == 0.008219178082
        assert pytest.approx(timeframe.get_duration('w')) == 0.428571428571
        assert pytest.approx(timeframe.get_duration('M')) == 0.1

        assert timeframe.get_duration('d') == 3
        assert timeframe.get_duration('h') == 72
        assert timeframe.get_duration('m') == 4320
        assert timeframe.get_duration('s') == 259200
        assert timeframe.get_duration('ms') == 259200000

    def test_get_duration_unit_is_invalid(self, timeframe):
        with pytest.raises(errors.UnknownTimeframeUnitError):
            timeframe.get_duration('some unknown unit')

    def test_get_pandas_timeframe(self, timeframe):
        assert timeframe.get_pandas_timeframe() == '3D'

    def test_repr_function(self, timeframe):
        assert repr(timeframe).startswith(f'{Timeframe.__name__}(')
        assert repr(timeframe).endswith(')')

        assert f'interval={timeframe.interval!r}' in repr(timeframe)
        assert f'unit={timeframe.unit!r}' in repr(timeframe)
        assert ',' in repr(timeframe)

    def test_str_function(self, timeframe):
        assert str(timeframe) == '3d'
