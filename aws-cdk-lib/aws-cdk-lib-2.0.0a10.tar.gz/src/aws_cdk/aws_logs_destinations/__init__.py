'''
# CDK Construct Libray for AWS XXX

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

A short description here.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from ..aws_kinesis import IStream as _IStream_4e2457d2
from ..aws_lambda import IFunction as _IFunction_6adb0ab8
from ..aws_logs import (
    ILogGroup as _ILogGroup_3c4fa718,
    ILogSubscriptionDestination as _ILogSubscriptionDestination_99a12804,
    LogSubscriptionDestinationConfig as _LogSubscriptionDestinationConfig_15877ced,
)


@jsii.implements(_ILogSubscriptionDestination_99a12804)
class KinesisDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_logs_destinations.KinesisDestination",
):
    '''(experimental) Use a Kinesis stream as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, stream: _IStream_4e2457d2) -> None:
        '''
        :param stream: -

        :stability: experimental
        '''
        jsii.create(KinesisDestination, self, [stream])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        _source_log_group: _ILogGroup_3c4fa718,
    ) -> _LogSubscriptionDestinationConfig_15877ced:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param _source_log_group: -

        :stability: experimental
        '''
        return typing.cast(_LogSubscriptionDestinationConfig_15877ced, jsii.invoke(self, "bind", [scope, _source_log_group]))


@jsii.implements(_ILogSubscriptionDestination_99a12804)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_logs_destinations.LambdaDestination",
):
    '''(experimental) Use a Lamda Function as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, fn: _IFunction_6adb0ab8) -> None:
        '''
        :param fn: -

        :stability: experimental
        '''
        jsii.create(LambdaDestination, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        log_group: _ILogGroup_3c4fa718,
    ) -> _LogSubscriptionDestinationConfig_15877ced:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param log_group: -

        :stability: experimental
        '''
        return typing.cast(_LogSubscriptionDestinationConfig_15877ced, jsii.invoke(self, "bind", [scope, log_group]))


__all__ = [
    "KinesisDestination",
    "LambdaDestination",
]

publication.publish()
