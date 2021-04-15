"""
Main interface for mediaconnect service client waiters.

Usage::

    ```python
    import boto3

    from mypy_boto3_mediaconnect import MediaConnectClient
    from mypy_boto3_mediaconnect.waiter import (
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
    )

    client: MediaConnectClient = boto3.client("mediaconnect")

    flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
    flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
    flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from mypy_boto3_mediaconnect.type_defs import WaiterConfigTypeDef

__all__ = ("FlowActiveWaiter", "FlowDeletedWaiter", "FlowStandbyWaiter")


class FlowActiveWaiter(Boto3Waiter):
    """
    [Waiter.FlowActive documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowActive)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [FlowActive.wait documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowActive.wait)
        """


class FlowDeletedWaiter(Boto3Waiter):
    """
    [Waiter.FlowDeleted documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowDeleted)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [FlowDeleted.wait documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowDeleted.wait)
        """


class FlowStandbyWaiter(Boto3Waiter):
    """
    [Waiter.FlowStandby documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowStandby)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [FlowStandby.wait documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.53/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowStandby.wait)
        """
