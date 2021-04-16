"""
Main interface for cloud9 service type definitions.

Usage::

    ```python
    from mypy_boto3_cloud9.type_defs import EnvironmentLifecycleTypeDef

    data: EnvironmentLifecycleTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EnvironmentLifecycleTypeDef",
    "EnvironmentMemberTypeDef",
    "EnvironmentTypeDef",
    "TagTypeDef",
    "CreateEnvironmentEC2ResultTypeDef",
    "CreateEnvironmentMembershipResultTypeDef",
    "DescribeEnvironmentMembershipsResultTypeDef",
    "DescribeEnvironmentStatusResultTypeDef",
    "DescribeEnvironmentsResultTypeDef",
    "ListEnvironmentsResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateEnvironmentMembershipResultTypeDef",
)

EnvironmentLifecycleTypeDef = TypedDict(
    "EnvironmentLifecycleTypeDef",
    {
        "status": Literal["CREATING", "CREATED", "CREATE_FAILED", "DELETING", "DELETE_FAILED"],
        "reason": str,
        "failureResource": str,
    },
    total=False,
)

_RequiredEnvironmentMemberTypeDef = TypedDict(
    "_RequiredEnvironmentMemberTypeDef",
    {
        "permissions": Literal["owner", "read-write", "read-only"],
        "userId": str,
        "userArn": str,
        "environmentId": str,
    },
)
_OptionalEnvironmentMemberTypeDef = TypedDict(
    "_OptionalEnvironmentMemberTypeDef", {"lastAccess": datetime}, total=False
)


class EnvironmentMemberTypeDef(
    _RequiredEnvironmentMemberTypeDef, _OptionalEnvironmentMemberTypeDef
):
    pass


_RequiredEnvironmentTypeDef = TypedDict(
    "_RequiredEnvironmentTypeDef", {"type": Literal["ssh", "ec2"], "arn": str, "ownerArn": str}
)
_OptionalEnvironmentTypeDef = TypedDict(
    "_OptionalEnvironmentTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "connectionType": Literal["CONNECT_SSH", "CONNECT_SSM"],
        "lifecycle": "EnvironmentLifecycleTypeDef",
        "managedCredentialsStatus": Literal[
            "ENABLED_ON_CREATE",
            "ENABLED_BY_OWNER",
            "DISABLED_BY_DEFAULT",
            "DISABLED_BY_OWNER",
            "DISABLED_BY_COLLABORATOR",
            "PENDING_REMOVAL_BY_COLLABORATOR",
            "PENDING_START_REMOVAL_BY_COLLABORATOR",
            "PENDING_REMOVAL_BY_OWNER",
            "PENDING_START_REMOVAL_BY_OWNER",
            "FAILED_REMOVAL_BY_COLLABORATOR",
            "FAILED_REMOVAL_BY_OWNER",
        ],
    },
    total=False,
)


class EnvironmentTypeDef(_RequiredEnvironmentTypeDef, _OptionalEnvironmentTypeDef):
    pass


TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

CreateEnvironmentEC2ResultTypeDef = TypedDict(
    "CreateEnvironmentEC2ResultTypeDef", {"environmentId": str}, total=False
)

CreateEnvironmentMembershipResultTypeDef = TypedDict(
    "CreateEnvironmentMembershipResultTypeDef", {"membership": "EnvironmentMemberTypeDef"}
)

DescribeEnvironmentMembershipsResultTypeDef = TypedDict(
    "DescribeEnvironmentMembershipsResultTypeDef",
    {"memberships": List["EnvironmentMemberTypeDef"], "nextToken": str},
    total=False,
)

DescribeEnvironmentStatusResultTypeDef = TypedDict(
    "DescribeEnvironmentStatusResultTypeDef",
    {
        "status": Literal[
            "error", "creating", "connecting", "ready", "stopping", "stopped", "deleting"
        ],
        "message": str,
    },
)

DescribeEnvironmentsResultTypeDef = TypedDict(
    "DescribeEnvironmentsResultTypeDef", {"environments": List["EnvironmentTypeDef"]}, total=False
)

ListEnvironmentsResultTypeDef = TypedDict(
    "ListEnvironmentsResultTypeDef", {"nextToken": str, "environmentIds": List[str]}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateEnvironmentMembershipResultTypeDef = TypedDict(
    "UpdateEnvironmentMembershipResultTypeDef",
    {"membership": "EnvironmentMemberTypeDef"},
    total=False,
)
