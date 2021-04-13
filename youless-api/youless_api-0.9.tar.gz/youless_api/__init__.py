"""
This file contains a helper class to easily obtain data from the YouLess sensor.
"""
from typing import Optional

import requests

from youless_api.devices import LS120, LS110, YouLessDevice
from youless_api.youless_sensor import YoulessSensor, PowerMeter

name = "youless_api"


class YoulessAPI:
    """A helper class to obtain data from the YouLess Sensor."""

    _device: Optional[YouLessDevice]

    def __init__(self, host):
        """Initialize the data bridge."""
        self._url = 'http://' + host
        self._device = None

    def initialize(self):
        """Establish a connection to the remote device"""
        response = requests.get(f"{self._url}/d")
        if response.ok:
            self._device = LS120(self._url, response.json())
        else:
            alive = requests.get(self._url)
            if alive.ok:
                self._device = LS110(self._url)

    def update(self):
        """Fetch the latest settings from the Youless Sensor."""
        if self._device:
            self._device.update()

    @property
    def mac_address(self):
        """Get the MAC address of the connected device."""
        if self._device is not None:
            return self._device.mac_address

        return None

    @property
    def model(self):
        """Return the model of the connected device."""
        if self._device is not None:
            return self._device.model

        return None

    @property
    def gas_meter(self):
        """"Get the gas data available."""
        if self._device is not None:
            return self._device.gas_meter

        return None

    @property
    def current_power_usage(self):
        """Get the current power usage."""
        if self._device is not None:
            return self._device.current_power_usage

        return None

    @property
    def power_meter(self):
        """Get the power meter values."""
        if self._device is not None:
            return self._device.power_meter

        return None

    @property
    def delivery_meter(self):
        """Get the power delivered values."""
        if self._device is not None:
            return self._device.delivery_meter

        return None

    @property
    def extra_meter(self):
        """Get the meter values of an attached meter."""
        if self._device is not None:
            return self._device.extra_meter

        return None
