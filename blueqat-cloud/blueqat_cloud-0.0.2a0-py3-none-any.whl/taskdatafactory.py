"""Module for making Task and TaskData.

This module is for internal use.
"""
import typing
from typing import Optional

from .device import Device
from .device_specific import aws_device
from .data import ExecutionRequest

if typing.TYPE_CHECKING:
    from blueqat import Circuit
    from .api import Api


def make_executiondata(c: 'Circuit',
                  dev: Device,
                  shots: int,
                  group: Optional[str] = None,
                  send_email: bool = False) -> ExecutionRequest:
    """Make ExecutionData for send job to the server."""
    if dev.value.startswith("aws/"):
        return aws_device.make_executiondata(c, dev, shots, group, send_email)
    raise ValueError(f"Cannot make {str(dev)} device task")
