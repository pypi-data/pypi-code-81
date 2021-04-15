"""Trading ETL OHLCV package."""

from trading.etl.ohlcv.core.metadata import OHLCVMetadata
from trading.etl.ohlcv.core.metadata import Timeframe
from trading.etl.ohlcv.core.ohlcv import OHLCV

# Don't expose core module in public package
# but expect name error from linting and tests
try:
    del core
except NameError:  # pragma: no cover
    pass
