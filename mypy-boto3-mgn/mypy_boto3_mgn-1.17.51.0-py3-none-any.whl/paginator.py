"""
Main interface for mgn service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_mgn import mgnClient
    from mypy_boto3_mgn.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceServersPaginator,
    )

    client: mgnClient = boto3.client("mgn")

    describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
    describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
    describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
    describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_mgn.type_defs import (
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestFiltersTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestFiltersTypeDef,
    DescribeSourceServersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceServersPaginator",
)


class DescribeJobLogItemsPaginator(Boto3Paginator):
    """
    [Paginator.DescribeJobLogItems documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobLogItems)
    """

    def paginate(
        self, jobID: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [DescribeJobLogItems.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobLogItems.paginate)
        """


class DescribeJobsPaginator(Boto3Paginator):
    """
    [Paginator.DescribeJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobs)
    """

    def paginate(
        self,
        filters: DescribeJobsRequestFiltersTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeJobsResponseTypeDef]:
        """
        [DescribeJobs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobs.paginate)
        """


class DescribeReplicationConfigurationTemplatesPaginator(Boto3Paginator):
    """
    [Paginator.DescribeReplicationConfigurationTemplates documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeReplicationConfigurationTemplates)
    """

    def paginate(
        self,
        replicationConfigurationTemplateIDs: List[str],
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [DescribeReplicationConfigurationTemplates.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        """


class DescribeSourceServersPaginator(Boto3Paginator):
    """
    [Paginator.DescribeSourceServers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeSourceServers)
    """

    def paginate(
        self,
        filters: DescribeSourceServersRequestFiltersTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeSourceServersResponseTypeDef]:
        """
        [DescribeSourceServers.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeSourceServers.paginate)
        """
