#!/usr/bin/env python3

# Copyright 2021 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Python interface to a `ThorLabs MC2000B <https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=287>`_
optical chopper unit.
"""

import logging
from enum import IntEnum
from threading import Lock
import re

import serial
from serial.tools import list_ports, list_ports_common

# There's two different types of reference input maps
_BLADE_INREFS_1 = ("internal-outer", "internal-inner", "external-outer", "external-inner")
_BLADE_INREFS_2 = ("internal", "external")
# ..and three types of reference outputs
_BLADE_OUTREFS_1 = ("target", "outer", "inner")
_BLADE_OUTREFS_2 = ("target", "actual")
_BLADE_OUTREFS_3 = ("target", "outer", "inner", "sum", "difference")


class Blade(IntEnum):
    """
    Mapping of chopping blade model numbers to the indices used by the underlying communications
    protocol.

    As this is an :class:`IntEnum`, the usual techniques apply.
    For example:

    .. code-block:: python

        Blade(6).name               # == "MC1F10HP"
        Blade(Blade.MC1F10HP).value # == 6
        Blade["MC1F10HP"]           # == Blade.MC1F10HP
    
    Additionally, the valid input and output reference sources for a blade model can be queried
    using the properties:

    .. code-block:: python

        Blade["MC1F10HP"].inrefs  # == ("internal-outer", "internal-inner", "external-outer", "external-inner")
        Blade["MC1F10HP"].outrefs # == ("target", "outer", "inner")
    """
    MC1F2    = 0
    MC1F10   = 1
    MC1F15   = 2
    MC1F30   = 3
    MC1F60   = 4
    MC1F100  = 5
    MC1F10HP = 6
    MC1F2P10 = 7
    MC1F6P10 = 8
    MC1F10A  = 9
    MC2F330  = 10
    MC2F47   = 11
    MC2F57B  = 12
    MC2F860  = 13
    MC2F5360 = 14


    @property
    def inrefs(self):
        """
        Get a tuple of valid internal reference source strings for this blade.
        """
        if self in (Blade.MC1F2, Blade.MC1F10HP, Blade.MC1F2P10):
            return _BLADE_INREFS_1
        elif self in (Blade.MC1F10, Blade.MC1F15, Blade.MC1F30, Blade.MC1F60, Blade.MC1F100, Blade.MC1F6P10, Blade.MC1F10A, Blade.MC2F330, Blade.MC2F47, Blade.MC2F57B, Blade.MC2F860, Blade.MC2F5360):
            return _BLADE_INREFS_2
        else:
            raise ValueError(f"{self} is not a valid Blade")
    
    @property
    def outrefs(self):
        """
        Get a tuple of valid output reference source strings for this blade.
        """
        if self in (Blade.MC1F2, Blade.MC1F10HP, Blade.MC1F2P10):
            return _BLADE_OUTREFS_1
        elif self in (Blade.MC1F10, Blade.MC1F15, Blade.MC1F30, Blade.MC1F60, Blade.MC1F100, Blade.MC1F6P10, Blade.MC1F10A):
            return _BLADE_OUTREFS_2
        elif self in (Blade.MC2F330, Blade.MC2F47, Blade.MC2F57B, Blade.MC2F860, Blade.MC2F5360):
            return _BLADE_OUTREFS_3
        else:
            raise ValueError(f"{self} is not a valid Blade")
            
    
# List of get/set properties and their description
_properties = {
    "freq"       : "internal reference frequency",
    "refoutfreq" : "reference output frequency",
    "blade"      : "blade type",
    "nharmonic"  : "harmonic multiplier",
    "dharmonic"  : "harmonic divider",
    "phase"      : "phase adjust",
    "enable"     : "enable",
    "ref"        : "reference mode",
    "output"     : "output reference mode",
    "oncycle"    : "on cycle",
    "intensity"  : "display intensity",
    "input"      : "current external reference frequency"
    }

class MC2000B():
    """
    Initialise and open serial device for the ThorLabs MC2000B Optical Chopper.

    The features of the chopper can be accessed using properties of this class.
    Valid properties are:

        * ``freq``       : internal reference frequency
        * ``refoutfreq`` : reference output frequency
        * ``blade``      : blade type
        * ``nharmonic``  : harmonic multiplier
        * ``dharmonic``  : harmonic divider
        * ``phase``      : phase adjust
        * ``enable``     : enable
        * ``ref``        : reference mode
        * ``output``     : output reference mode
        * ``oncycle``    : on cycle
        * ``intensity``  : display intensity
        * ``input``      : current external reference frequency
    
    See the chopper's manual for more detailed descriptions of these features.
    
    Example usage may be something like:

    .. code-block:: python

        from thorlabs_mc2000b import MC2000B
        # Initialise the first detected device
        chopper = MC2000B()
        # We'll assume the default MC1F10HP is installed
        print(chopper.get_blade_string())
        # Set up to use external reference source and the inner part of the blade
        chopper.set_inref_string("external-inner")
        # Apply a 1/2 divider to the input frequency
        chopper.nharmonic = 1
        chopper.dharmonic = 2
        # Start it up!
        chopper.enable = True

    If the ``serial_port`` parameter is ``None`` (default), then an attempt to detect a MC2000B
    will be performed.
    The first device found will be initialised.
    If multiple devices are present on the system, then the use of the ``serial_number`` parameter
    will specify a particular device by its serial number.
    This is a `regular expression <https://docs.python.org/3/library/re.html>`_ match, for example
    ``serial_number="21"`` would match devices with serial numbers
    starting with 21, while ``serial_number=".*21$"`` would match devices ending in 21.

    :param serial_port: Serial port device the chopper is connected to.
    :param serial_number: Regular expression matching the serial number of device to search for.
    """

    def __init__(self, serial_port=None, serial_number=""):

        # If serial_port not specified, search for a device
        if serial_port is None:
            serial_port = find_device(serial_number=serial_number)

        # Accept a serial.tools.list_ports.ListPortInfo object (which we may have just found)
        if isinstance(serial_port, list_ports_common.ListPortInfo):
            serial_port = serial_port.device

        if serial_port is None:
            raise RuntimeError(f"No Thorlabs MC2000B devices detected.")
        
        # Lock to only allow single query to serial port at a time (from multiple threads)
        self._sp_lock = Lock()
        self._log = logging.getLogger(__name__)
        self._log.info(f"Initialising serial port ({serial_port}).")
        # Open and configure serial port settings
        self._sp = serial.Serial(port=serial_port,
                         baudrate=115200,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS,
                         timeout=0.2,
                         write_timeout=0.2)
        self._log.info("Opened serial port OK.")

        # Check if device is a MC2000B
        reply = self._send_command("id?")
        if reply[0:16] != "THORLABS MC2000B":
            raise RuntimeError(f"Could not query MC2000B information! (device responded with {reply})")
        self.id = reply

    def __del__(self):
        self.close()

    def __getattr__(self, name):
        """Intercept __getattr__ calls for valid chopper properties."""
        if name in _properties:
            return self._get_property(name)
        else:
            raise AttributeError(f"Attempt to get invalid property '{name}' for MC2000B")

    def __setattr__(self, name, value):
        """Intercept __setattr__ calls for valid chopper properties."""
        if name in _properties:
            self._set_property(name, value)
        else:
            super().__setattr__(name, value)

    def _send_command(self, command_string):
        """
        Write a command out the the serial port, wait for response and return the received string.

        A carriage return (CR) will be appended to the given command_string.
        """
        if self._sp == None:
            raise RuntimeError("Can't communicate with MC2000B as serial port has been closed!")
        command_string = command_string + "\r"
        self._log.debug(f"Writing command string: {command_string}")
        self._sp.write(bytearray(command_string, "ascii"))
        indata = ""
        while indata[-3:] != "\r> ":
            try:
                inbytes = self._sp.read(1)
            except serial.SerialException:
                self._log.warning(f"Error reading reply string! (requested {command_string}, received {indata})")
                break
            if len(inbytes) > 0:
                indata += inbytes.decode("ascii")
            else:
                self._log.warning(f"Timeout reading reply string! (requested {command_string}, received {indata})")
                break
        self._log.debug(f"Received reply string: {indata}")
        if indata[0:len(command_string)] != command_string:
            self._log.warning(f"Command not echoed in reply string! (requested {command_string}, received {indata})")
        else:
            indata = indata[len(command_string):-3]
        return indata.replace("\r", "\n")

    def _get_property(self, prop):
        """Request a property value from the chopper."""
        if not prop in _properties:
            raise RuntimeError(f"Attempt to get invalid property '{prop}' of MC2000B")
        self._sp_lock.acquire()
        try:
            # Dodgy hack to work around buggy serial communications at high command rates
            self._send_command("")
            reply = self._send_command(prop + "?")
        finally: self._sp_lock.release()
        try:
            reply = int(reply)
        except:
            raise RuntimeError(f"Could not get MC2000B {_properties[prop]} (requested '{prop}?', received {reply})!")
        return reply

    def _set_property(self, prop, value):
        """Set a property value for the chopper."""
        if not prop in _properties:
            raise RuntimeError(f"Attempt to set invalid property '{prop}' of MC2000B")
        if prop in ("refoutfreq", "input"):
            raise RuntimeError(f"Attempt to set read-only property '{prop}' of MC2000B")
        try:
            value = int(float(value))
        except:
            RuntimeError(f"Attempt to set invalid value for property '{prop}' of MC2000B ('{value}' is not a number)")
        try:
            # Dodgy hack to work around buggy serial communications at high command rates
            self._sp_lock.acquire()
            self._send_command("")
            reply = self._send_command(f"{prop}={value}")
        finally: self._sp_lock.release()
        if reply:
            raise RuntimeError(f"Could not set MC2000B {_properties[prop]} (requested '{prop}={value}', received {reply})!")

    def get_commands(self):
        """Returns a string containing the list of possible commands the chopper understands."""
        self._sp_lock.acquire()
        reply = self._send_command("?")
        self._sp_lock.release()
        return reply

    def get_inref_string(self):
        """Return the current input reference source as a string."""
        return Blade(self.blade).inrefs[self.ref]

    def set_inref_string(self, value):
        """
        Configure the input reference source using a string.
        Not all values are valid for every chopper wheel type, and an exception will be raised if an invalid reference type is requested.
        Valid types can be obtained by looking at the appropriate :data:`Blade.inrefs` property, for example, ``Blade(Blade.MC1F10HP).inrefs``
        or ``Blade["MC1F10HP"].inrefs`` for the default MC1F10HP model blade.

        :param value: String describing the input reference source, one of ``internal``, ``external``, ``internal-outer``, ``internal-inner``, ``external-outer``, ``external-inner``.
        :raises: RuntimeError if invalid value requested.
        """
        if not value in Blade(self.blade).inrefs:
            raise RuntimeError(f"Invalid input reference type '{value}' for MC2000B current blade {Blade(self.blade).name}!\nValid values are {Blade(self.blade).inrefs}")
        self._set_property("ref", Blade(self.blade).inrefs.index(value))

    def get_outref_string(self):
        """Return the current output reference source as a string."""
        return Blade(self.blade).outrefs[self.output]

    def set_outref_string(self, value):
        """
        Configure the output reference source using a string.
        Not all values are valid for every chopper wheel type --- an exception will be raised if an invalid reference type is requested.
        Valid types can be obtained by looking at the appropriate :data:`Blade.outrefs` property, for example, ``Blade(Blade.MC1F10HP).outrefs``
        or ``Blade["MC1F10HP"].outrefs`` for the default MC1F10HP model blade.

        :param value: String describing the output reference source, one of ``target``, ``actual``, ``outer``, ``inner``, ``sum``, ``difference``.
        :raises: RuntimeError if invalid value requested.
        """
        if not value in Blade(self.blade).outrefs:
            raise RuntimeError(f"Invalid output reference type '{value}' for MC2000B current blade {Blade(self.blade).name}!\nValid values are {Blade(self.blade).outrefs}")
        self._set_property("output", Blade(self.blade).outrefs.index(value))

    def get_blade_string(self):
        """Return the current blade model as a string."""
        return Blade(self.blade).name

    def close(self):
        """Close the serial connection to the chopper."""
        if self._sp != None:
            self._sp.close()
            self._sp = None
            self._log.info("Closed serial port.")

def find_device(serial_number=""):
    """
    Search attached serial ports for a Thorlabs MC2000B.

    The first device found will be returned.
    If multiple choppers are attached to the system, the ``serial_number`` parameter may be used
    to select the correct device. This is a regular expression match, for example
    ``serial_number="21"`` would match devices with serial numbers starting with 21, while
    ``serial_number=".*21$"`` would match devices ending in 21.

    :param serial_number: Regular expression to match a device serial number.
    """
    for p in serial.tools.list_ports.comports():
        # If manufacturer and product fields exist, try to use them
        # We require a match on serial number though
        if ((re.match("Thorlabs", p.manufacturer) if p.manufacturer else True)
            and (re.match("MC2000B", p.product) if p.product else True)
            and (re.match(serial_number, p.serial_number) if p.serial_number else False)):
            return p


