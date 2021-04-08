from dataclasses import dataclass
from inspect import signature
from typing import Any

# TODO check fields on TCP and RTU for types
from sunspec2.modbus.client import SunSpecModbusClientDeviceTCP, SunSpecModbusClientDeviceRTU


@dataclass
class ConnectOptionsTcp:
    slave_id: int = signature(SunSpecModbusClientDeviceTCP).parameters["slave_id"].default
    ip_address: str = signature(SunSpecModbusClientDeviceTCP).parameters["ipaddr"].default
    ip_port: int = signature(SunSpecModbusClientDeviceTCP).parameters["ipport"].default
    timeout: float = None
    ctx: Any = None
    max_count: int = signature(SunSpecModbusClientDeviceTCP).parameters["max_count"].default
    test: bool = signature(SunSpecModbusClientDeviceTCP).parameters["test"].default


@dataclass
class ConnectOptionsRtu:
    slave_id: int
    name: str
    baudrate: int = None
    parity: str = None
    timeout: float = None
    ctx: Any = None
    max_count: int = signature(SunSpecModbusClientDeviceRTU).parameters["max_count"].default


@dataclass
class ConnectOptionsFile:
    filename: str = None
    addr: int = 40000


@dataclass
class ConnectOptions:
    file: ConnectOptionsFile = None
    tcp: ConnectOptionsTcp = None
    rtu: ConnectOptionsRtu = None
