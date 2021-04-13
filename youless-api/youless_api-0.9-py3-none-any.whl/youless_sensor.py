"""

This file contains the sensor class for the youless API

"""


class YoulessSensor:
    """A wrapper class to contain the Youless Sensor values."""

    def __init__(self, value, uom):
        """Initialize the value wrapper."""
        self._value = value
        self._uom = uom

    @property
    def unit_of_measurement(self):
        """Get the unit of measurement for this value."""
        return self._uom

    @property
    def value(self):
        """Get the current value"""
        return self._value


class PowerMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor,
                 total: YoulessSensor):
        self._low = low
        self._high = high
        self._total = total

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    @property
    def total(self):
        return self._total


class DeliveryMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor):
        self._low = low
        self._high = high

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high


class ExtraMeter:

    def __init__(self, total: YoulessSensor, usage: YoulessSensor):
        self._total = total
        self._usage = usage

    def usage(self) -> YoulessSensor:
        return self._usage

    def total(self) -> YoulessSensor:
        return self._total


