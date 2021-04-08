import logging
from contextlib import contextmanager

import sunspec2.file.client as file_client
import sunspec2.modbus.client as client

from pysunspec_read.connect_options import ConnectOptions

logger = logging.getLogger(__name__)


@contextmanager
def read(connect_options: ConnectOptions):
    device = connect(connect_options)
    logger.info("Reading from device")
    device.scan()
    try:
        yield device
    finally:
        if connect_options.file is None:
            logger.info("Closing device connection")
            device.close()


def connect_file(file):
    logger.info("Connecting to file as input, name=%s, address=%s", file.filename, file.addr)
    return file_client.FileClientDevice(filename=file.filename)


def connect_rtu(rtu):
    logger.info("Connecting to device using device type=rtu, name=%s, baudrate=%s, parity=%s, timeout=%s",
                rtu.name,
                rtu.baudrate,
                rtu.parity,
                rtu.timeout)
    return client.SunSpecModbusClientDeviceRTU(slave_id=rtu.slave_id,
                                               name=rtu.name,
                                               baudrate=rtu.baudrate,
                                               parity=rtu.parity,
                                               timeout=rtu.timeout,
                                               ctx=rtu.ctx,
                                               max_count=rtu.max_count)


def connect_tcp(tcp):
    logger.info("Connecting to device using device type=tcp, ip=%s, port=%s, slave_id=%s, timeout=%s",
                tcp.ip_address,
                tcp.ip_port,
                tcp.slave_id,
                tcp.timeout)
    return client.SunSpecModbusClientDeviceTCP(slave_id=tcp.slave_id,
                                               ipaddr=tcp.ip_address,
                                               ipport=tcp.ip_port,
                                               timeout=tcp.timeout,
                                               ctx=tcp.ctx,
                                               test=tcp.test,
                                               max_count=tcp.max_count)


def connect(connect_options: ConnectOptions):
    if connect_options.tcp is not None:
        return connect_tcp(connect_options.tcp)
    elif connect_options.rtu is not None:
        return connect_rtu(connect_options.rtu)
    elif connect_options.file is not None:
        return connect_file(connect_options.file)
    else:
        raise NameError("No connect option supplied")
