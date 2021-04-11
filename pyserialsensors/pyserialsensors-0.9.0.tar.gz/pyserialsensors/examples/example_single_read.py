# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Example script for running a measurement using i2c senors only.
"""

from pySerialMeasurement.devices.FTDI import init_all
from pySerialMeasurement.tools.bulk import setup, ThreadWithReturnValue
from pySerialMeasurement.core.i2controller import MmsI2cController
from pySerialMeasurement.core.i2controller import MmsSpiController

import logging

# logging.basicConfig(level=logging.ERROR)


def reinitialize():
    for m in dev.mux:
        for s in m.sensors:
            if s["obj"] is not None:
                s["obj"].prepare_measurement()


def runMeasurement(setup):
    for dev in setup:
        if isinstance(dev, MmsI2cController):
            for mux in dev.mux:
                for sensor in mux.sensors:
                    if sensor["obj"] is not None:
                        val = sensor["obj"].prepare_measurement()
        elif isinstance(dev, MmsSpiController):
            for sensor in dev.sensors:
                val = sensor["obj"].prepare_measurement()

    for i in range(3000):
        for dev in setup:
            if isinstance(dev, MmsI2cController):
                for mux in dev.mux:
                    for sensor in mux.sensors:
                        if sensor["obj"] is not None:
                            val = sensor["obj"].get_data()
                            if sensor["obj"].disconnected_ftdi:
                                # if a ftdi disconnected all sensors have
                                # to be reinitialized
                                reinitialize(dev)
                                s["obj"].disconnected_ftdi = False
                            val = sensor["obj"].get_data()
                            out = f"{val['sensor_type']: >10}"
                            if val["serialno"] is None:
                                out += f"{'': >20}"
                            else:
                                out += f"{val['serialno']: >20}"
                            if "values" in val:
                                for value in val["values"]:
                                    v = val["values"][value]["value"]
                                    u = val["values"][value]["unit"]
                                    res = f"{v: 0.2f} {u}"
                                    out += f"{res: >20}"
                            else:
                                out += "Reading error"

                    print(out)

            elif isinstance(dev, MmsSpiController):
                for sensor in dev.sensors:
                    val = sensor["obj"].get_data()
                    out = f"{val['sensor_type']: >10}"

                    if val["serialno"] is None:
                        out += f"{'': >20}"
                    else:
                        out += f"{val['serialno']: >20}"
                    if "values" in val:
                        for qty in val["values"]:
                            if val["values"][qty]["value"] is not None:
                                v = val["values"][qty]["value"]
                                u = val["values"][qty]["unit"]
                                res = f"{v: 0.2f} {u}"
                                out += f"{res: >20}"
                            else:
                                out += "\t Reading error"

                    print(out)


if __name__ == "__main__":
    log = logging.getLogger("exampleThreading")
    Bus = []
    setups = []
    CS_MUX = True

    # Check how many serial converters are connected
    supported_converters = [(0x0403, 0x6014)]
    dev = init_all(supported_converters, CS_MUX=CS_MUX)

    log.info("Found %s FTDI", len(dev))
    for d in dev:
        Bus.append(d)

    threads = []
    for bus in Bus:
        j = ThreadWithReturnValue(target=setup, args=(bus,))
        j.start()
        threads.append(j)
    for t in threads:
        setups.append(t.join())

    threads = []
    if len(setups) > 0:
        for s in setups:
            if s is not None:
                j = ThreadWithReturnValue(target=runMeasurement, args=(s,))
                j.start()
                threads.append(j)
    else:
        raise SystemError("No FTDI found.")

    for t in threads:
        j.join()
