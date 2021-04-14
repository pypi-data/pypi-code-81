from ctypes import c_uint8, c_uint16, c_uint32, cast, pointer, POINTER
from ctypes import create_string_buffer, Structure
from fcntl import ioctl
import struct
import os
import sys
import pydopi.devmem as devmem 
class i2c_msg(Structure):
    """Linux i2c_msg struct."""
    _fields_ = [
        ("addr", c_uint16),
        ("flags", c_uint16),
        ("len", c_uint16),
        ("buf", POINTER(c_uint8)),
    ]
class i2c_rdwr_ioctl_data(Structure):  # pylint: disable=invalid-name
    """Linux i2c data struct."""
    _fields_ = [("msgs", POINTER(i2c_msg)), ("nmsgs", c_uint32)]

class I2C(object):
    # ctypes versions of I2C structs defined by kernel.
    # Tone down pylint for the Python classes that mirror C structs.
    # pylint: disable=invalid-name,too-few-public-methods



    # pylint: enable=invalid-name,too-few-public-methods


    def __make_i2c_rdwr_data(self,messages):
        """Utility function to create and return an i2c_rdwr_ioctl_data structure
        populated with a list of specified I2C messages.  The messages parameter
        should be a list of tuples which represent the individual I2C messages to
        send in this transaction.  Tuples should contain 4 elements: address value,
        flags value, buffer length, ctypes c_uint8 pointer to buffer.
        """
        # Create message array and populate with provided data.
        msg_data_type = i2c_msg * len(messages)
        msg_data = msg_data_type()
        for i, message in enumerate(messages):
            msg_data[i].addr = message[0] & 0x7F
            msg_data[i].flags = message[1]
            msg_data[i].len = message[2]
            msg_data[i].buf = message[3]
        # Now build the data structure.
        data = i2c_rdwr_ioctl_data()
        data.msgs = msg_data
        data.nmsgs = len(messages)
        return data

    
    def __init__(self, bus=2, addr=0x12):
        # I2C C API constants (from linux kernel headers)
        self.__I2C_M_TEN = 0x0010  # this is a ten bit chip address
        self.__I2C_M_RD = 0x0001  # read data, from slave to master
        self.__I2C_M_STOP = 0x8000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_NOSTART = 0x4000  # if I2C_FUNC_NOSTART
        self.__I2C_M_REV_DIR_ADDR = 0x2000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_IGNORE_NAK = 0x1000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_NO_RD_ACK = 0x0800  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_RECV_LEN = 0x0400  # length will be first received byte

        self.__I2C_SLAVE = 0x0703  # Use this slave address
        self.__I2C_SLAVE_FORCE = 0x0706  # Use this slave address, even if
        # is already in use by a driver!
        self.__I2C_TENBIT = 0x0704  # 0 for 7 bit addrs, != 0 for 10 bit
        self.__I2C_FUNCS = 0x0705  # Get the adapter functionality mask
        self.__I2C_RDWR = 0x0707  # Combined R/W transfer (one STOP only)
        self.__I2C_PEC = 0x0708  # != 0 to use PEC with SMBus
        self.__I2C_SMBUS = 0x0720  # SMBus transfer
        self.dev = None
        self.open(bus, addr)
    def open(self,bus=2, addr=0x12):
        self.close()
        if bus == 0:
            self.sda_addr = 0x112C0030
            self.scl_addr = 0x112C0034
        elif bus == 1:
            self.sda_addr = 0x112C00A0
            self.scl_addr = 0x112C00A4
        elif bus == 2:
            self.sda_addr = 0x112C0038
            self.scl_addr = 0x112C003c
        val = devmem.read(self.sda_addr)
        devmem.write(self.sda_addr, (val &0xFFFFFFF0)|0x1)
        val = devmem.read(self.scl_addr)
        devmem.write(self.scl_addr, (val &0xFFFFFFF0)|0x1)
        self.dev = open("/dev/i2c-{0}".format(bus), "r+b", buffering=0)
        self.addr = addr
    def __del__(self):
        self.close()
    def close(self):
        if self.dev is not None:
            self.dev.close()
            self.dev = None
    def read(self, cmd):
        """Read a single byte from the specified cmd register of the device."""
        assert (
            self.dev is not None
        ), "Bus must be opened before operations are made against it!"
        # Build ctypes values to marshall between ioctl and Python.
        reg = c_uint8(cmd)
        result = c_uint8()
        # Build ioctl request.
        request = self.__make_i2c_rdwr_data(
            [
                (self.addr, 0, 1, pointer(reg)),  # Write cmd register.
                (self.addr, self.__I2C_M_RD, 1, pointer(result)),  # Read 1 byte as result.
            ]
        )
        # Make ioctl call and return result data.
        ioctl(self.dev.fileno(), self.__I2C_RDWR, request)
        return result.value
    def write(self, cmd, val):
        """Write a byte of data to the specified cmd register of the device.
        """
        assert (
            self.dev is not None
        ), "Bus must be opened before operations are made against it!"
        # Construct a string of data to send with the command register and byte value.
        data = bytearray(2)
        data[0] = cmd & 0xFF
        data[1] = val & 0xFF
        # Send the data to the device.
        ioctl(self.dev.fileno(), self.__I2C_SLAVE, self.addr & 0x7F)
        self.dev.write(data)