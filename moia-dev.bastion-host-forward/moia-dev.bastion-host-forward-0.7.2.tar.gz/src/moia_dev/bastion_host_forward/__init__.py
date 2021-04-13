'''
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmoia-dev%2Fbastion-host-forward%2Fbadge&style=for-the-badge)](https://actions-badge.atrox.dev/moia-dev/bastion-host-forward/goto)
[![NPM](https://flat.badgen.net/npm/v/@moia-dev/bastion-host-forward)](https://www.npmjs.com/package/@moia-dev/bastion-host-forward)

# Bastion Host Forward

This CDK Library provides custom constructs `BastionHostRDSForward` and
`BastionHostRedisForward`. It's an extension for the `BastionHostLinux`, which
forwards traffic from an RDS Instance or Redis in the same VPC. This makes it
possible to connect to a service inside a VPC from a developer machine outside of
the VPC via the AWS Session Manager. The library allows connections to a
basic-auth RDS via username and password or IAM, as well as to Redis clusters.

# Setup

First of all you need to include this library into your project for the language
you want to deploy the bastion host with

## Javascript/Typescript

For Javascript/Typescript the library can be installed via npm:

```
npm install @moia-dev/bastion-host-forward
```

## Python

For python the library can be installed via pip:

```
pip install moia-dev.bastion-host-forward
```

# Examples

The following section includes some examples in supported languages how the
Bastion Host can be created for different databases.

## Creating the Bastion Host for RDS in Typescript

A minimal example for creating the RDS Forward Construct, which will be used via
username/password could look like this snippet:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from aws_cdk.aws_ec2 import SecurityGroup, Vpc
from aws_cdk.aws_rds import DatabaseInstance
from moia_dev.bastion_host_rds_forward import BastionHostRDSForward

class BastionHostPocStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        vpc = Vpc.from_lookup(self, "MyVpc",
            vpc_id="vpc-0123456789abcd"
        )

        security_group = SecurityGroup.from_security_group_id(self, "RDSSecurityGroup", "odsufa5addasdj", mutable=False)

        rds_instance = DatabaseInstance.from_database_instance_attributes(self, "MyDb",
            instance_identifier="abcd1234geh",
            instance_endpoint_address="abcd1234geh.ughia8asd.eu-central-1.rds.amazonaws.com",
            port=5432,
            security_groups=[security_group]
        )

        BastionHostRDSForward(self, "BastionHost",
            vpc=vpc,
            rds_instance=rds_instance,
            name="MyBastionHost"
        )
```

If the RDS is IAM Authenticated you also need to add an `iam_user` and
`rdsResourceIdentifier` to the BastionHostRDSForward:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
BastionHostRDSForward(self, "BastionHost",
    vpc=vpc,
    rds_instance=rds_instance,
    name="MyBastionHost",
    iam_user="iamusername",
    rds_resource_identifier="db-ABCDEFGHIJKL123"
)
```

This will spawn a Bastion Host in the defined VPC. You also need to make sure
that IPs from within the VPC are able to connect to the RDS Database. This
needs to be set in the RDS's Security Group. Otherwise the Bastion Host can't
connect to the RDS.

## Creating the Bastion Host for Redis in Typescript

The instantiation of a BastionHostRedisForward works very similar to the RDS
example, except that you pass a CfnCacheCluster to the BastionHost like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
BastionHostRedisForward(self, "RedisBastion",
    elasticache_cluster=cluster,
    vpc=vpc
)
```

## Creating the Bastion Host for Redshift

### Typescript

A minimal example for creating the Redshift Forward Construct, which will be used via
username/password could look like this snippet. It's very similar to the RDS
version. The only difference is that we need a Redshift Cluster object instead
of a RDS DatabaseInstance:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from moia_dev.bastion_host_forward import BastionHostRedshiftForward
from aws_cdk.aws_ec2 import SecurityGroup, Vpc
from aws_cdk.aws_redshift import Cluster

class PocRedshiftStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        vpc = Vpc.from_lookup(self, "MyVpc",
            vpc_id="vpc-12345678"
        )

        security_group = SecurityGroup.from_security_group_id(self, "BastionHostSecurityGroup", "sg-1245678,", mutable=False)

        redshift_cluster = Cluster.from_cluster_attributes(self, "RedshiftCluster",
            cluster_name="myRedshiftClusterName",
            cluster_endpoint_address="myRedshiftClusterName.abcdefg.eu-central-1.redshift.amazonaws.com",
            cluster_endpoint_port=5439
        )

        BastionHostRedshiftForward(self, "BastionHostRedshiftForward",
            vpc=vpc,
            name="MyRedshiftBastionHost",
            security_group=security_group,
            redshift_cluster=redshift_cluster
        )
```

### Python

```python
from aws_cdk import core as cdk
from aws_cdk import aws_redshift
from aws_cdk import aws_ec2
from moia_dev import bastion_host_forward


class PocRedshiftStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = aws_ec2.Vpc.from_lookup(
            self,
            "vpc",
            vpc_id="vpc-12345678"
        )
        security_group = aws_ec2.SecurityGroup.from_security_group_id(
            self,
            "sec_group", "sg-12345678"
        )
        redshiftCluster = aws_redshift.Cluster.from_cluster_attributes(
            self,
            "cluster",
            cluster_name="myRedshiftClusterName",
            cluster_endpoint_address="myRedshiftClusterName.abcdefg.eu-central-1.redshift.amazonaws.com",
            cluster_endpoint_port=5439
        )

        bastion_host_forward.BastionHostRedshiftForward(
            self,
            "bastion-host",
            name="my-vastion-host",
            security_group=security_group,
            redshift_cluster=redshiftCluster,
            vpc=vpc
        )
```

## Deploying the Bastion Host

When you setup the Bastion Host for the Database you want to connect to, you can
now go forward to actually deploy the Bastion Host:

```
cdk deploy
```

When the EC2 Instance for you Bastion Host is visible you can continue with the
setup of the Session-Manager Plugin on your Machine

# Install the Session-Manager Plugin for AWS-CLI

You are also able to connect to the Bastion Host via the AWS Web
Console. For this go to `AWS Systems Manager` -> `Session Manager` -> choose
the newly created instance -> click on start session.

But overall it's a much more comfortable experience to connect to the Bastion
Session Manager Plugin. On Mac OSX you can get it via homebrew for example:

```
brew cask install session-manager-plugin
```

For Linux it should also be available in the respective package manager. Also
have a look at [the official installation instructions from
AWS](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

## Forward the connection to your machine

The Session Manager offers a command to forward a specific port. On the Bastion
Host a HAProxy was installed which forwards the connection on the same
port as the specified service. Those are by default:

* RDS: 5432
* Redis: 6739
* Redshift: 5439

In the following example, we show how to forward the connection of a PostgreSQL
database. To forward the connection to our machine we execute the following
command in the shell:

```
aws ssm start-session \
    --target <bastion-host-id> \
    --document-name AWS-StartPortForwardingSession \
    --parameters '{"portNumber": ["5432"], "localPortNumber":["5432"]}'
```

This creates a port forward session on the defined `localPortNumber`. The
target is the id of the bastion host instance. This will be output
automatically after deploying the bastion host. The `portNumber` must be the
same as the RDS Port.

Now you would be able to connect to the RDS as it would run on localhost:5432.

## Additional step if you are using IAM Authentication on RDS

If you have an IAM authenticated RDS, the inline policy of the bastion
host will be equipped with access rights accordingly. Namely it will get `rds:*`
permissions on the RDS you provided and it also allows `rds-db:connect` with
the provided `iamUser`.

Most of the steps you would perform to connect to the RDS are the same, since it wouldn't
be in a VPC.

First you generate the PGPASSWORD on your local machine:

```
export
PGPASSWORD="$(aws rds generate-db-auth-token
--hostname=<rds endpoint> --port=5432
--username=<iam user> --region <the region of the rds>)"
```

You also need to have the RDS certificate from AWS, which you can download:

```
wget https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem
```

There is now an additional step needed, because the certificate checks against
the real endpoint name during the connect procedure. Therefore we need to add
an entry to the `/etc/hosts` file on our machine:

```
echo "127.0.0.1  <rds endpoint>" >> /etc/hosts
```

Now you can connect to the IAM authenticated RDS like this:

```
psql "host=<rds endpoint> port=5432 dbname=<database name> user=<iamUser> sslrootcert=<full path to downloaded cert> sslmode=verify-ca"
```

For a full guide on how to connect to an IAM authenticated RDS check out [this
guide by AWS](https://aws.amazon.com/premiumsupport/knowledge-center/users-connect-rds-iam/)
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
import aws_cdk.aws_rds
import aws_cdk.aws_redshift
import aws_cdk.core


class BastionHostForward(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@moia-dev/bastion-host-forward.BastionHostForward",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        address: builtins.str,
        port: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param address: The address of the service to forward to.
        :param port: The port of the service to forward to.
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        props = BastionHostForwardProps(
            address=address,
            port=port,
            vpc=vpc,
            client_timeout=client_timeout,
            name=name,
            security_group=security_group,
        )

        jsii.create(BastionHostForward, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bastionHost")
    def _bastion_host(self) -> aws_cdk.aws_ec2.BastionHostLinux:
        '''
        :return: The BastionHost Instance
        '''
        return typing.cast(aws_cdk.aws_ec2.BastionHostLinux, jsii.get(self, "bastionHost"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''
        :return:

        the id of the bastion host, which can be used by the session
        manager connect command afterwards
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "instanceId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''
        :return: the security group attached to the bastion host
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], jsii.get(self, "securityGroup"))

    @security_group.setter
    def security_group(
        self,
        value: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup],
    ) -> None:
        jsii.set(self, "securityGroup", value)


@jsii.data_type(
    jsii_type="@moia-dev/bastion-host-forward.BastionHostForwardBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "client_timeout": "clientTimeout",
        "name": "name",
        "security_group": "securityGroup",
    },
)
class BastionHostForwardBaseProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        '''
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if name is not None:
            self._values["name"] = name
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The Vpc in which to instantiate the Bastion Host.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The HAProxy client timeout in minutes.

        :default: 1
        '''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bastionHost instance.

        :default: "BastionHost"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''The security group, which is attached to the bastion host.

        :default:

        If none is provided a default security group is attached, which
        doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostForwardBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@moia-dev/bastion-host-forward.BastionHostForwardProps",
    jsii_struct_bases=[BastionHostForwardBaseProps],
    name_mapping={
        "vpc": "vpc",
        "client_timeout": "clientTimeout",
        "name": "name",
        "security_group": "securityGroup",
        "address": "address",
        "port": "port",
    },
)
class BastionHostForwardProps(BastionHostForwardBaseProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        address: builtins.str,
        port: builtins.str,
    ) -> None:
        '''
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        :param address: The address of the service to forward to.
        :param port: The port of the service to forward to.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "address": address,
            "port": port,
        }
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if name is not None:
            self._values["name"] = name
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The Vpc in which to instantiate the Bastion Host.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The HAProxy client timeout in minutes.

        :default: 1
        '''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bastionHost instance.

        :default: "BastionHost"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''The security group, which is attached to the bastion host.

        :default:

        If none is provided a default security group is attached, which
        doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def address(self) -> builtins.str:
        '''The address of the service to forward to.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The port of the service to forward to.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostForwardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BastionHostRDSForward(
    BastionHostForward,
    metaclass=jsii.JSIIMeta,
    jsii_type="@moia-dev/bastion-host-forward.BastionHostRDSForward",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        rds_instance: aws_cdk.aws_rds.IDatabaseInstance,
        iam_user: typing.Optional[builtins.str] = None,
        rds_resource_identifier: typing.Optional[builtins.str] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param rds_instance: -
        :param iam_user: -
        :param rds_resource_identifier: -
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        props = BastionHostRDSForwardProps(
            rds_instance=rds_instance,
            iam_user=iam_user,
            rds_resource_identifier=rds_resource_identifier,
            vpc=vpc,
            client_timeout=client_timeout,
            name=name,
            security_group=security_group,
        )

        jsii.create(BastionHostRDSForward, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@moia-dev/bastion-host-forward.BastionHostRDSForwardProps",
    jsii_struct_bases=[BastionHostForwardBaseProps],
    name_mapping={
        "vpc": "vpc",
        "client_timeout": "clientTimeout",
        "name": "name",
        "security_group": "securityGroup",
        "rds_instance": "rdsInstance",
        "iam_user": "iamUser",
        "rds_resource_identifier": "rdsResourceIdentifier",
    },
)
class BastionHostRDSForwardProps(BastionHostForwardBaseProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        rds_instance: aws_cdk.aws_rds.IDatabaseInstance,
        iam_user: typing.Optional[builtins.str] = None,
        rds_resource_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        :param rds_instance: -
        :param iam_user: -
        :param rds_resource_identifier: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "rds_instance": rds_instance,
        }
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if name is not None:
            self._values["name"] = name
        if security_group is not None:
            self._values["security_group"] = security_group
        if iam_user is not None:
            self._values["iam_user"] = iam_user
        if rds_resource_identifier is not None:
            self._values["rds_resource_identifier"] = rds_resource_identifier

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The Vpc in which to instantiate the Bastion Host.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The HAProxy client timeout in minutes.

        :default: 1
        '''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bastionHost instance.

        :default: "BastionHost"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''The security group, which is attached to the bastion host.

        :default:

        If none is provided a default security group is attached, which
        doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def rds_instance(self) -> aws_cdk.aws_rds.IDatabaseInstance:
        result = self._values.get("rds_instance")
        assert result is not None, "Required property 'rds_instance' is missing"
        return typing.cast(aws_cdk.aws_rds.IDatabaseInstance, result)

    @builtins.property
    def iam_user(self) -> typing.Optional[builtins.str]:
        result = self._values.get("iam_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rds_resource_identifier(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rds_resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostRDSForwardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BastionHostRedisForward(
    BastionHostForward,
    metaclass=jsii.JSIIMeta,
    jsii_type="@moia-dev/bastion-host-forward.BastionHostRedisForward",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        address: builtins.str,
        port: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param address: The address of the service to forward to.
        :param port: The port of the service to forward to.
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        props = BastionHostForwardProps(
            address=address,
            port=port,
            vpc=vpc,
            client_timeout=client_timeout,
            name=name,
            security_group=security_group,
        )

        jsii.create(BastionHostRedisForward, self, [scope, id, props])


class BastionHostRedshiftForward(
    BastionHostForward,
    metaclass=jsii.JSIIMeta,
    jsii_type="@moia-dev/bastion-host-forward.BastionHostRedshiftForward",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        redshift_cluster: aws_cdk.aws_redshift.ICluster,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param redshift_cluster: -
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        props = BastionHostRedshiftForwardProps(
            redshift_cluster=redshift_cluster,
            vpc=vpc,
            client_timeout=client_timeout,
            name=name,
            security_group=security_group,
        )

        jsii.create(BastionHostRedshiftForward, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@moia-dev/bastion-host-forward.BastionHostRedshiftForwardProps",
    jsii_struct_bases=[BastionHostForwardBaseProps],
    name_mapping={
        "vpc": "vpc",
        "client_timeout": "clientTimeout",
        "name": "name",
        "security_group": "securityGroup",
        "redshift_cluster": "redshiftCluster",
    },
)
class BastionHostRedshiftForwardProps(BastionHostForwardBaseProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        client_timeout: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        redshift_cluster: aws_cdk.aws_redshift.ICluster,
    ) -> None:
        '''
        :param vpc: The Vpc in which to instantiate the Bastion Host.
        :param client_timeout: The HAProxy client timeout in minutes. Default: 1
        :param name: The name of the bastionHost instance. Default: "BastionHost"
        :param security_group: The security group, which is attached to the bastion host. Default: If none is provided a default security group is attached, which doesn't allow incoming traffic and allows outbound traffic to everywhere
        :param redshift_cluster: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "redshift_cluster": redshift_cluster,
        }
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if name is not None:
            self._values["name"] = name
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The Vpc in which to instantiate the Bastion Host.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The HAProxy client timeout in minutes.

        :default: 1
        '''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bastionHost instance.

        :default: "BastionHost"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''The security group, which is attached to the bastion host.

        :default:

        If none is provided a default security group is attached, which
        doesn't allow incoming traffic and allows outbound traffic to everywhere
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def redshift_cluster(self) -> aws_cdk.aws_redshift.ICluster:
        result = self._values.get("redshift_cluster")
        assert result is not None, "Required property 'redshift_cluster' is missing"
        return typing.cast(aws_cdk.aws_redshift.ICluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostRedshiftForwardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BastionHostForward",
    "BastionHostForwardBaseProps",
    "BastionHostForwardProps",
    "BastionHostRDSForward",
    "BastionHostRDSForwardProps",
    "BastionHostRedisForward",
    "BastionHostRedshiftForward",
    "BastionHostRedshiftForwardProps",
]

publication.publish()
