# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

import sys
import glob
import serial
import logging


def search_comports():
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    _logger = logging.getLogger("search_comports")

    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    _logger.debug("Found %d ports.", len(ports))
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException) as e:
            if "Permission" in str(e):
                _logger.info("No permission to read %s", len(result))
            pass
    _logger.info("Found %d devices.", len(result))

    return result


if __name__ == "__main__":
    print(serial_ports())
