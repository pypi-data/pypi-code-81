import json
from typing import Mapping, Optional, Sequence

import pulumi
import pulumi_aws.s3 as s3
from pulumi import ComponentResource, ResourceOptions

from ..utils import validate_principal


class BucketPutPermissionsArgs:
    def __init__(self, principal: str, paths: Optional[Sequence[str]] = None) -> None:
        validate_principal(principal)
        self.principal = principal
        if paths:
            if not isinstance(paths, list):
                raise TypeError("paths must be of type list")
            for path in paths:
                if not isinstance(path, str):
                    raise TypeError("Each path must be of type str")
                if not path.startswith("/") or not path.endswith("/"):
                    raise ValueError("Each path must start and end with '/'")
        self.paths = paths


class Bucket(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        name: str,
        lifecycle_rules: Sequence[s3.BucketLifecycleRuleArgs] = None,
        put_permissions: Optional[Sequence[BucketPutPermissionsArgs]] = None,
        tags: Mapping[str, str] = None,
        versioning: Optional[s3.BucketVersioningArgs] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            t="data-engineering-pulumi-components:aws:Bucket",
            name=resource_name,
            props=None,
            opts=opts,
        )
        if not isinstance(resource_name, str):
            raise TypeError("resource_name must be of type str")
        if not isinstance(name, str):
            raise TypeError("name must be of type str")

        self._bucket = s3.Bucket(
            resource_name=f"{resource_name}-bucket",
            acl=s3.CannedAcl.PRIVATE,
            bucket=name,
            force_destroy=False,
            lifecycle_rules=lifecycle_rules,
            server_side_encryption_configuration={
                "rule": {
                    "applyServerSideEncryptionByDefault": {"sseAlgorithm": "AES256"}
                }
            },
            tags=tags,
            versioning=versioning,
            opts=ResourceOptions(parent=self),
        )
        self._bucketPublicAccessBlock = s3.BucketPublicAccessBlock(
            resource_name=f"{resource_name}-bucket-public-access-block",
            bucket=self._bucket.id,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
            opts=ResourceOptions(parent=self._bucket),
        )

        def get_policy(args):
            bucket_arn, put_permissions = args

            all_principals = []
            statements = []
            for item in put_permissions:
                all_principals.append(item.principal)
                statements.append(
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": [item.principal]},
                        "Action": ["s3:PutObject", "s3:PutObjectAcl"],
                        "Resource": [bucket_arn + path + "*" for path in item.paths]
                        if item.paths
                        else [bucket_arn + "/*"],
                    }
                )
            statements.extend(
                [
                    {
                        "Effect": "Deny",
                        "Principal": {"AWS": all_principals},
                        "Action": ["s3:PutObject"],
                        "Resource": [bucket_arn + "/*"],
                        "Condition": {
                            "StringNotEquals": {
                                "s3:x-amz-acl": ["bucket-owner-full-control"],
                            },
                        },
                    },
                    {
                        "Effect": "Deny",
                        "Principal": {"AWS": all_principals},
                        "Action": ["s3:PutObject"],
                        "Resource": [bucket_arn + "/*"],
                        "Condition": {
                            "StringNotEquals": {
                                "s3:x-amz-server-side-encryption": ["AES256"],
                            },
                        },
                    },
                    {
                        "Effect": "Deny",
                        "Principal": {"AWS": all_principals},
                        "Action": ["s3:PutObject"],
                        "Resource": [bucket_arn + "/*"],
                        "Condition": {
                            "Null": {"s3:x-amz-server-side-encryption": ["true"]},
                        },
                    },
                ]
            )

            return json.dumps({"Version": "2012-10-17", "Statement": statements})

        if put_permissions:
            policy = pulumi.Output.all(self._bucket.arn, put_permissions).apply(
                get_policy
            )
            self._bucketPolicy = s3.BucketPolicy(
                resource_name=f"{resource_name}-bucket-policy",
                bucket=self._bucket.id,
                policy=policy,
                opts=ResourceOptions(parent=self._bucket),
            )

        outputs = {
            "arn": self._bucket.arn,
            "id": self._bucket.id,
            "name": self._bucket.bucket,
        }

        for name, value in outputs.items():
            setattr(self, name, value)

        self.register_outputs(outputs)
