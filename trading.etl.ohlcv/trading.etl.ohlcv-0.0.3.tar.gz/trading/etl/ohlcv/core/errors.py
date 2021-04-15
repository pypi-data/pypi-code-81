"""Module containing OHLCV-related errors."""

class InvalidTimeframeError(ValueError):
    """This error is raised when the input timeframe is invalid
    or can't be automagically extrapolated from the input."""


class UnknownTimeframeUnitError(ValueError):
    """This error is raised when the input timeframe unit is unknown."""


class DBQueryGenerationError(Exception):
    """This error is raised when we failed to generate a DB query."""


class OHLCVFetchError(Exception):
    """This error is raised when we failed to fetch OHLCV from DB."""
