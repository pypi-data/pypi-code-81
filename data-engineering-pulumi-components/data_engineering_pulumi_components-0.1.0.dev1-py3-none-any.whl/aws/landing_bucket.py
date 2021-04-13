from typing import Mapping, Optional

from pulumi import ResourceOptions

from data_engineering_pulumi_components.aws.bucket import (
    Bucket,
    BucketPutPermissionsArgs,
)


class LandingBucket(Bucket):
    def __init__(
        self,
        resource_name: str,
        name: str,
        aws_arn_for_put_permission: str,
        tags: Mapping[str, str] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            resource_name=resource_name + "-landing",
            name=name + "-landing",
            put_permissions=[BucketPutPermissionsArgs(aws_arn_for_put_permission)],
            tags=tags,
            opts=opts,
        )
