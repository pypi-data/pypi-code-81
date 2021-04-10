from enum import Enum
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, validator


class Interval(str, Enum):
    i1m = "1m"
    i2m = "2m"
    i5m = "5m"
    i15m = "15m"
    i30m = "30m"
    i60m = "60m"
    i90m = "90m"
    i1h = "1h"
    i1d = "1d"
    i5d = "5d"
    i1wk = "1wk"
    i1mo = "1mo"
    i3mo = "3mo"


class Range(str, Enum):
    r1d = "1d"
    r5d = "5d"
    r1mo = "1mo"
    r3mo = "3mo"
    r6mo = "6mo"
    r1y = "1y"
    r2y = "2y"
    r5y = "5y"
    r10y = "10y"
    rytd = "ytd"
    rmax = "max"


class CustomRange(BaseModel):
    period1: datetime
    period2: datetime

    @validator("period2")
    def validate_periods(
        cls, period2: datetime, values: Dict[str, datetime]
    ) -> datetime:
        """Validates the period2 field making sure it is before period1.

        Args:
            period2: The date time to validate.
            values: The other values of the object.

        Returns:
            The period2 as is if valid.

        Raises:
            ValueError: If the end date time starts before the start date time.
        """
        if period2 < values["period1"]:
            raise ValueError("period2 cannot be less than period1")
        return period2