'''
[![NPM version](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2.svg)](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2)
[![PyPI version](https://badge.fury.io/py/super-ec2.svg)](https://badge.fury.io/py/super-ec2)
![Release](https://github.com/cdk-constructs-zone/super-ec2/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/@cdk-constructs-zone/super-ec2?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/super-ec2?label=pypi&color=blue)

![](https://img.shields.io/badge/jenkins-ec2-green=?style=plastic&logo=appveyor)

# Welcome to `@cdk-constructs-zone/super-ec2`

This repository template helps you create EC2 .

## Note
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.core


@jsii.enum(jsii_type="@cdk-constructs-zone/super-ec2.AmiOSType")
class AmiOSType(enum.Enum):
    '''
    :stability: experimental
    '''

    UBUNTU_18_04 = "UBUNTU_18_04"
    '''(experimental) Ubuntu 18.04 ami.

    :stability: experimental
    '''
    UBUNTU_20_04 = "UBUNTU_20_04"
    '''(experimental) Ubuntu 20.04 ami.

    :stability: experimental
    '''
    CENTOS_7 = "CENTOS_7"
    '''(experimental) CentOS 7 ami.

    :stability: experimental
    '''
    CENTOS_8 = "CENTOS_8"
    '''(experimental) CentOS 8 ami.

    :stability: experimental
    '''
    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    '''(experimental) Amazon Linux 2 ami.

    :stability: experimental
    '''
    AMAZON_LINUX = "AMAZON_LINUX"
    '''(experimental) Amazon Linux  ami.

    :stability: experimental
    '''


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.ISuperEC2BaseProps")
class ISuperEC2BaseProps(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ISuperEC2BasePropsProxy"]:
        return _ISuperEC2BasePropsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="amiOSType")
    def ami_os_type(self) -> typing.Optional[AmiOSType]:
        '''(experimental) Super EC2 OS you want.

        :default: - Amzaon Linux 2.

        :stability: experimental
        '''
        ...

    @ami_os_type.setter
    def ami_os_type(self, value: typing.Optional[AmiOSType]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        '''(experimental) Super EC2 Instance Type.

        :default: - t3.small.

        :stability: experimental
        '''
        ...

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[aws_cdk.aws_ec2.InstanceType],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''(experimental) Super EC2 Vpc.

        :default: - Create a new Vpc.

        :stability: experimental
        '''
        ...

    @vpc.setter
    def vpc(self, value: typing.Optional[aws_cdk.aws_ec2.IVpc]) -> None:
        ...


class _ISuperEC2BasePropsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.ISuperEC2BaseProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="amiOSType")
    def ami_os_type(self) -> typing.Optional[AmiOSType]:
        '''(experimental) Super EC2 OS you want.

        :default: - Amzaon Linux 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AmiOSType], jsii.get(self, "amiOSType"))

    @ami_os_type.setter
    def ami_os_type(self, value: typing.Optional[AmiOSType]) -> None:
        jsii.set(self, "amiOSType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        '''(experimental) Super EC2 Instance Type.

        :default: - t3.small.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.InstanceType], jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[aws_cdk.aws_ec2.InstanceType],
    ) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''(experimental) Super EC2 Vpc.

        :default: - Create a new Vpc.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: typing.Optional[aws_cdk.aws_ec2.IVpc]) -> None:
        jsii.set(self, "vpc", value)


class SuperEC2Base(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdk-constructs-zone/super-ec2.SuperEC2Base",
):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_SuperEC2BaseProxy"]:
        return _SuperEC2BaseProxy

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: ISuperEC2BaseProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        jsii.create(SuperEC2Base, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultSecurityGroup")
    def default_security_group(self) -> aws_cdk.aws_ec2.SecurityGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.SecurityGroup, jsii.get(self, "defaultSecurityGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instance")
    def instance(self) -> aws_cdk.aws_ec2.IInstance:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IInstance, jsii.get(self, "instance"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userData")
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.UserData, jsii.get(self, "userData"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))


class _SuperEC2BaseProxy(SuperEC2Base):
    pass


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.IJenkinsEC2Props")
class IJenkinsEC2Props(ISuperEC2BaseProps, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IJenkinsEC2PropsProxy"]:
        return _IJenkinsEC2PropsProxy


class _IJenkinsEC2PropsProxy(
    jsii.proxy_for(ISuperEC2BaseProps) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.IJenkinsEC2Props"
    pass


class JenkinsEC2(
    SuperEC2Base,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-constructs-zone/super-ec2.JenkinsEC2",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: typing.Optional[IJenkinsEC2Props] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        jsii.create(JenkinsEC2, self, [scope, id, props])

    @jsii.member(jsii_name="jenkinsUserData")
    def jenkins_user_data(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "jenkinsUserData", []))


__all__ = [
    "AmiOSType",
    "IJenkinsEC2Props",
    "ISuperEC2BaseProps",
    "JenkinsEC2",
    "SuperEC2Base",
]

publication.publish()
