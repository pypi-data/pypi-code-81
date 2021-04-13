import pulumi
from pulumi_aws.s3 import BucketVersioningArgs

from ..utils import Tagger
from .bucket import Bucket


class PulumiBackend(Bucket):
    def __init__(self, project_name: str, environment_name: str) -> None:
        # @TODO add the tagger policy files to validate the tags that are added
        tagger = Tagger(environment_name)
        derived_name = f"{project_name}-pulumi-backend"
        super().__init__(
            resource_name=derived_name,
            name=derived_name,
            lifecycle_rules=None,
            put_permissions=None,
            tags=tagger.create_tags(project_name),
            versioning=BucketVersioningArgs(enabled=True),
            opts=pulumi.ResourceOptions(protect=True),
        )
