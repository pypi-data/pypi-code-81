from typing import Mapping, Optional

from pulumi import ResourceOptions

from data_engineering_pulumi_components.aws.bucket import Bucket


class RawHistoryBucket(Bucket):
    def __init__(
        self,
        resource_name: str,
        name: str,
        tags: Mapping[str, str] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            resource_name=resource_name + "-raw-history",
            name=name + "-raw-history",
            tags=tags,
            versioning={"enabled": True},
            opts=opts,
        )
