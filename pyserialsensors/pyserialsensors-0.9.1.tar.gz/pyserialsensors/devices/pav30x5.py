# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Sensor Class for Posifa PAV30x5D
Tested with PAV3005D
Cuited for PAV3005D and PAV3015D
"""

import time
import logging
from .MUX import TCA9548 as MUX
from ..core.error import Error


class PAV30x5(object):
    __name__ = "PAV30x5"
    _serial_mode = "I2C"
    __clk_stretch = False
    _serial_mode = "I2C"
    _units = {
        "velocity": "m/s",
    }

    # PAV30x5 default address.
    _SENSOR_ADDRESS = 0x28
    __delay = 2e-2
    __max_attempts = 5
    _i2c_freq = 5e3

    # Operating Modes

    def __init__(self, i2cbus, mux_address, mux_port, sensor_id=None, **kwargs):
        """
        :param i2cbus: [OBJECT] like i2c.configure('ftdi://ftdi:232h/1')
        from pyftdi.i2c
        :param mux_address: [STRING] ic2 address of the sensor or multiplexer
        :param mux_port: [INTEGER] multiplexer port number
        :param sensor_id: [STRING] identifier or name of the sensor
        :param **kwargs: [DICT] additional setting
                sensor_address: [STRING] i2c address of the sensor
                mux_delay: [FLOAT] time difference for commands
                for the multiplexer communication
        """
        self.error = None
        self._address = kwargs.get("address", self.__SENSOR_ADDRESS)

        self.ftdi_serial = kwargs.get("ftdi_serial", None)
        self._logger = logging.getLogger("PAV30x5.PAV30x5")

        # Holds last result
        self.data = {}

        # Setup MUX
        self.mux = MUX(i2cbus, mux_address)
        self.mux_address = mux_address
        self.mux_port = mux_port
        self.sensor_id = sensor_id
        self.sensor_type = "PAV30x5"
        self.mux.close_all_ports()

        # Setup Sensor
        self.sensor = self.mux.i2cbus.get_port(self.__SENSOR_ADDRESS)
        self.reset()
        self.serial_number = None
        self.error = None
        self.exists = self.sensor_exists()
        self.t_fine = 0.0

    def __str__(self):
        out = "PAV30x5@"
        out += f"FTDI_ {self.ftdi_serial}"
        out += f":MUX_{self.mux_address}.{self.mux_port}"
        return out

    def get_serial_number(self):
        return 10

    def reset(self):
        pass

    def sensor_exists(self):
        """
        test if sensor is plugged in and works proper
        :return: [BOOLEAN] True if test was successful otherwise False
        """
        val = False
        val = self.txrx(cmd=[0xD0], readlen=6)
        time.sleep(0.5)
        val = self.read(readlen=7)
        print(val)

        if not val:
            return True
        else:
            self.error = Error().read(self)
            return False

    def crc(self, ba):
        """
        Compute check sum: 1 + ~(sum data bytes)
        PAV30x5 see Application note i2C Specification prosifa Dec 2019
        """
        res = None
        if ba:
            checksum = ba[0]
            val = [ba[1], ba[2]]
            s = 0
            for v in val:
                s += v
            res = (checksum + ~(s % 256)) % 256

        return res

    def read(self, readlen=6):
        ba = self.mux.receive(self.sensor, readlength=readlen, port=self.mux_port)
        crc = self.crc(ba)
        if not crc:
            return None

        time.sleep(self.__delay)
        return ba

    def txrx(self, cmd, readlen=3):
        """
        write cmd, read readlen bytes from i2c, perform crc check.
        If successful return data else False
        :param cmd:  [bytearray] i2c command
        :param readlen: [integer] number of bytes to read
        """

        # WR
        ba = self.mux.exchange(self.sensor, cmd, port=self.mux_port, readlength=readlen)
        crc = self.crc(ba)
        if not crc:
            return None
        time.sleep(self.__delay)

        # check if data was received
        return ba

    def getU16(self, cmd):
        """
        Read an unsigned 16-bit value from the specified register, in little
        endian byte order.
        """
        out = self.txrx(cmd, readlen=2)
        if out:
            return (out[1] << 8) | out[0]
        return None

    def getS16(self, cmd):
        """
        Read an unsigned 16-bit value from the specified register, in little
        endian byte order.
        """
        out = self.getU16(cmd)
        if out:
            if out > 32767:
                out -= 65536
            return out
        else:
            return None

    def getU8(self, cmd):
        """
        Read an unsigned 8-bit value from the specified register, in little
        endian byte order.
        """
        out = self.txrx(cmd, readlen=1)
        if out:
            return out[0]
        return False

    def getS8(self, cmd):
        """
        Read an signed 8-bit value from the specified register, in little
        endian byte order.
        """
        out = self.getU8(cmd)
        if out and out > 127:
            out -= 256
        return out

    def start_continuous_measurement(self):
        pass

    def get_data(self):
        """
        :param scale_factor: [INT] sensor specific parameter for the
        calculation of the volume flow
        :param offset: [INT] sensor specific parameter for the
        calculation of the volume flow
        :return: [DICT] data dictionary
        """
        # Wait until data is ready
        self.mux.i2cbus._ftdi.enable_adaptive_clock(self.__clk_stretch)
        self.error = None
        self.data = {
            "object": "DATA",
            "sensor_type": self.sensor_type,
            "error": True,
            "serialno": self.serial_number,
            "id": self.sensor_id,
            "FTDIserial": self.ftdi_serial,
            "MUXaddress": str(hex(self.mux.address)),
            "MUXport": str(self.mux_port),
        }

        try:
            U = self.read_velocity()
        except TypeError:
            # Throw an error if not able to fetch data
            self.mux.close_all_ports()
            self.error = Error().read(self)
            self.data["object"] = "ERROR"
            return self.data

        if self.error is None:
            self.data["error"] = False
            self.data["values"] = {}
            self.data["values"]["velocity"] = {
                "value": U,
                "unit": self._units["velocity"],
            }
            return self.data

    def read_velocity(self):
        """Returns the velocity value from the sensor."""
        ba = self.txrx()
        return ba
