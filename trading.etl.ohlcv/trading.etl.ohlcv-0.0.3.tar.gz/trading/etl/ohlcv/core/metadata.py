"""Module containing OHLCV metadata classes."""

from typing import Optional
from trading.etl.ohlcv.core import errors


__all__ = [
    # Class exports
    'Timeframe',
    'OHLCVMetadata',
]

UNIT_TO_SECONDS_MAPPING = {
    'y': 60 * 60 * 24 * 365,  # 31536000
    'M': 60 * 60 * 24 * 30,   # 2592000
    'w': 60 * 60 * 24 * 7,    # 604800
    'd': 60 * 60 * 24,        # 86400
    'h': 60 * 60,             # 3600
    'm': 60,                  # 60
    's': 1,                   # 1
    'ms': 1 / 1000,           # 0.001
}

# Create an inverse dictionary of conversion
SECONDS_TO_UNIT_MAPPING = {v: k for k, v in UNIT_TO_SECONDS_MAPPING.items()}

PANDAS_UNITS_MAPPING = {
    'M': 'MS',
    'w': 'W',
    'd': 'D',
    'h': 'H',
    'm': 'T',
    's': 'S',
    'ms': 'L',
}


class Timeframe:
    """Data class for timeframes."""

    def __init__(
        self,
        interval=None,
        unit: Optional[str] = None,
    ):

        if not interval and interval != 0:
            self.interval = None
            self.unit = None

        elif isinstance(interval, Timeframe):
            self.interval = interval.interval
            self.unit = interval.unit

        elif isinstance(interval, str):
            # Input interval is the whole timeframe, ignore unit argument
            if not interval.isdigit():
                self.interval = interval[:-1]
                self.unit = interval[-1]

            # Input interval is just the interval, use the unit argument
            else:
                self.interval = interval
                self.unit = unit

        # Unable to extrapolate, raise error
        else:
            raise errors.InvalidTimeframeError(f'{interval!r}, {unit!r}')

    def __repr__(self):
        return (f'{__class__.__name__}('
                f'interval={self.interval!r}, '
                f'unit={self.unit!r})')

    def __str__(self):
        return f'{self.interval}{self.unit if self.unit else ""}'

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        if not value and value != 0:
            self._interval = None
        else:
            self._interval = int(value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if not value:
            self._unit = None
            return

        value = str(value)
        if value not in UNIT_TO_SECONDS_MAPPING:
            raise errors.UnknownTimeframeUnitError(value)

        self._unit = value

    def get_duration(self, unit: str = 'ms') -> float:
        """Converts the given timefram into a duration in the target unit.

        Arguments:
            unit: The target unit of time that we want the duration
                in. Valid input values are `'y'`, `'M'`, `'w'`, `'d'`,
                `'h'`, `'m'`, `'s'`, and `'ms'`.

        Raises:
            UnknownTimeframeUnitError: Raised if the target unit is unknown.

        Return:
            A floating number representing the duration of the timeframe
            in the target unit of time.
        """
        duration_in_seconds = UNIT_TO_SECONDS_MAPPING[self.unit]
        duration_in_seconds *= self.interval

        if unit not in UNIT_TO_SECONDS_MAPPING:
            raise errors.UnknownTimeframeUnitError(unit)

        duration_in_target_unit = UNIT_TO_SECONDS_MAPPING[unit]
        duration_in_target_unit = 1 / duration_in_target_unit
        duration_in_target_unit *= duration_in_seconds

        return duration_in_target_unit

    def get_pandas_timeframe(self):
        """Returns the equivalent timeframe in Pandas's own units."""
        return f'{self.interval}{PANDAS_UNITS_MAPPING[self.unit]}'


class OHLCVMetadata:
    """Data class for OHLCV-related metadata."""

    def __init__(
        self,
        exchange: Optional[str] = None,
        symbol: Optional[str] = None
    ):
        self.exchange = exchange
        self.symbol = symbol

    def __repr__(self):
        return (f'{__class__.__name__}('
                f'exchange={self._exchange!r}, '
                f'symbol={self._symbol!r})')

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, value):
        if not value:
            self._exchange = None
        else:
            self._exchange = str(value)

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if not value:
            self._symbol = None
        else:
            self._symbol = str(value)
