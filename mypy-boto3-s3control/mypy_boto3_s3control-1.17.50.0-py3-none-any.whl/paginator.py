"""
Main interface for s3control service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_s3control import S3ControlClient
    from mypy_boto3_s3control.paginator import (
        ListAccessPointsForObjectLambdaPaginator,
    )

    client: S3ControlClient = boto3.client("s3control")

    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_s3control.type_defs import (
    ListAccessPointsForObjectLambdaResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListAccessPointsForObjectLambdaPaginator",)


class ListAccessPointsForObjectLambdaPaginator(Boto3Paginator):
    """
    [Paginator.ListAccessPointsForObjectLambda documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda)
    """

    def paginate(
        self, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccessPointsForObjectLambdaResultTypeDef]:
        """
        [ListAccessPointsForObjectLambda.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda.paginate)
        """
