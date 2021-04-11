# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

# ######################################################################################################################
# FILE: FTDIsensirion
#
# DESCRIPTION : Sensor Class for SDP6xx and SDP5xx
#
# VERSION : 1.0
#
# AUTHOR : konstantin.niehaus@dlr.de
#
# LAST UPDATE : May 8th 2019
#
# NEEDS : pyftdi
#
# ######################################################################################################################

from pyftdi.i2c import I2cController
from pyftdi.usbtools import UsbTools
from datetime import datetime
import warnings
import time
import configparser

from devices.MUX import TCA9548 as MUX
from core.error import Error

try:
    import struct
except ImportError:
    import ustruct as struct


class SDP6XX:
    """
    SDP6xx/5xx pressure sensor class
    """

    __SENSOR_ADDRESS = 0x40
    __max_attempts = 5
    __delay = 0.4
    __cmd_read = [0xF1]
    __cmd_soft_rst = [0xFE]
    __cmd_serial_number = None
    __scale_factor = {
        "SDP6xx-500Pa": 1 / 60.0,
        "SDP5xx": 1 / 60.0,
        "SDP6x0-125Pa": 1 / 240.0,
        "SDP6xx-25Pa": 1 / 1200.0,
    }

    def __init__(
        self,
        i2cbus,
        mux_address,
        mux_port,
        sensor_type="SDP6xx",
        sensor_id=None,
        **kwargs
    ):
        """
        :param i2cbus: [OBJECT] like i2c.configure('ftdi://ftdi:232h/1') from pyftdi.i2c
        :param mux_address: [STRING] ic2 address of the sensor or multiplexer
        :param mux_port: [INTEGER] multiplexer port number
        :param sensor_id: [STRING] identifier or name of the sensor
        :param **kwargs: [DICT] additional setting
                sensor_address: [STRING] i2c address of the sensor
                mux_delay: [FLOAT] time difference for commands for the multiplexer communication
                sensor_delay: [FLOAT] time difference for the sensor communication
        """
        ## Identifiers
        i2cbus._ftdi.enable_adaptive_clock("True")
        self.ftdi_serial = kwargs.get("ftdi_serial", None)
        self.mux = MUX(i2cbus, mux_address)
        self.mux_port = mux_port
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type

        # SENSOR INIT
        self.measurement_result = {}
        self.test_method = self.test_read

        self.mux.close_all_ports()
        self.sensor = self.mux.i2cbus.get_port(self.__SENSOR_ADDRESS)
        self.reset()
        self.serial_number = "not supported"
        self.error = None
        self.exists = self.sensor_exists()

    def sensor_exists(self):
        """
        test if sensor is plugged on and works proper
        :return: [BOOLEAN] True if test was successful otherwise False
        """
        resp = self.test_method()
        if resp:
            return True
        else:
            self.error = resp
            return False

    def reset(self):
        """
        reseting the sensor
        :return: True for successful reset else False
        """
        try:
            self.mux.send(self.sensor, self.__cmd_soft_rst, port=self.mux_port)
            time.sleep(self.__delay)
            return True
        except IOError:
            return False

    def get_serial_number(self):
        """
        Dummy function: SDP6xx and SDP5xx does not support serial number requests via I2C.
        :return: [STRING] not supported
        :raises: Warning
        """
        self.serial_number = "not supported"
        warnings.warn("SDP600 does not support serial number requests via I2C.")

    def start_continuous_measurement(self):
        """
        Dummy function: SDP6xx and SDP5xx does not support continuous measurements.
        :return: [STRING] not supported
        :raises: Warning
        """
        self.serial_number = "not supported"
        warnings.warn("SDP600 does not support continuous measurements.")

    def test_read(self):
        self.mux.send(self.sensor, self.__cmd_read, port=self.mux_port)
        ba = self.mux.receive(self.sensor, readlength=3, port=self.mux_port)
        if ba is not None:
            return True
        return False

    def get_data(self):
        """
        :param scale_factor: [INT] sensor specific parameter for the calculation of the volume flow
        :param offset: [INT] sensor specific parameter for the calculation of the volume flow
        :return: [DICT] data dictionary
        """
        self.mux.send(self.sensor, self.__cmd_read, port=self.mux_port)
        ba = self.mux.receive(self.sensor, readlength=3, port=self.mux_port)
        if ba:
            if Error().checksum(
                byte_values=[ba[0], ba[1]], crc_value=ba[2], crc_init=0x00
            )[1]:
                value, crc = struct.unpack(">HB", ba)
                if self.sensor_type in self.__scale_factor:
                    pressure = round(value / self.__scale_factor[self.sensor_type], 3)
                else:
                    pressure = value

                self.measurement_result = {
                    "object": "DATA",
                    "sensor_type": self.sensor_type,
                    "pressure": pressure,
                    "unit": "Pa",
                    "serialno": self.serial_number,
                    "id": self.sensor_id,
                    "FTDIserial": self.ftdi_serial,
                    "MUXaddress": str(hex(self.mux.address)),
                    "MUXport": self.mux_port,
                }
                return self.measurement_result

        self.mux.close_all_ports()
        self.error = Error().read(
            ftdi=self.ftdi_serial,
            mux=str(hex(self.mux.address)),
            mux_port=self.mux_port,
            sensor_id=self.sensor_id,
        )
        return self.error
