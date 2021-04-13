"""
Main interface for mgn service client

Usage::

    ```python
    import boto3
    from mypy_boto3_mgn import mgnClient

    client: mgnClient = boto3.client("mgn")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_mgn.paginator import (
    DescribeJobLogItemsPaginator,
    DescribeJobsPaginator,
    DescribeReplicationConfigurationTemplatesPaginator,
    DescribeSourceServersPaginator,
)
from mypy_boto3_mgn.type_defs import (
    ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestFiltersTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestFiltersTypeDef,
    DescribeSourceServersResponseTypeDef,
    LaunchConfigurationTypeDef,
    LicensingTypeDef,
    ListTagsForResourceResponseTypeDef,
    ReplicationConfigurationReplicatedDiskTypeDef,
    ReplicationConfigurationTemplateTypeDef,
    ReplicationConfigurationTypeDef,
    SourceServerTypeDef,
    StartCutoverResponseTypeDef,
    StartTestResponseTypeDef,
    TerminateTargetInstancesResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("mgnClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UninitializedAccountException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class mgnClient:
    """
    [mgn.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.can_paginate)
        """

    def change_server_life_cycle_state(
        self, lifeCycle: ChangeServerLifeCycleStateSourceServerLifecycleTypeDef, sourceServerID: str
    ) -> "SourceServerTypeDef":
        """
        [Client.change_server_life_cycle_state documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.change_server_life_cycle_state)
        """

    def create_replication_configuration_template(
        self,
        associateDefaultSecurityGroup: bool,
        bandwidthThrottling: int,
        createPublicIP: bool,
        dataPlaneRouting: Literal["PRIVATE_IP", "PUBLIC_IP"],
        defaultLargeStagingDiskType: Literal["GP2", "ST1"],
        ebsEncryption: Literal["NONE", "DEFAULT", "CUSTOM"],
        replicationServerInstanceType: str,
        replicationServersSecurityGroupsIDs: List[str],
        stagingAreaSubnetId: str,
        stagingAreaTags: Dict[str, str],
        useDedicatedReplicationServer: bool,
        ebsEncryptionKeyArn: str = None,
        tags: Dict[str, str] = None,
    ) -> "ReplicationConfigurationTemplateTypeDef":
        """
        [Client.create_replication_configuration_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.create_replication_configuration_template)
        """

    def delete_job(self, jobID: str) -> Dict[str, Any]:
        """
        [Client.delete_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.delete_job)
        """

    def delete_replication_configuration_template(
        self, replicationConfigurationTemplateID: str
    ) -> Dict[str, Any]:
        """
        [Client.delete_replication_configuration_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.delete_replication_configuration_template)
        """

    def delete_source_server(self, sourceServerID: str) -> Dict[str, Any]:
        """
        [Client.delete_source_server documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.delete_source_server)
        """

    def describe_job_log_items(
        self, jobID: str, maxResults: int = None, nextToken: str = None
    ) -> DescribeJobLogItemsResponseTypeDef:
        """
        [Client.describe_job_log_items documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.describe_job_log_items)
        """

    def describe_jobs(
        self,
        filters: DescribeJobsRequestFiltersTypeDef,
        maxResults: int = None,
        nextToken: str = None,
    ) -> DescribeJobsResponseTypeDef:
        """
        [Client.describe_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.describe_jobs)
        """

    def describe_replication_configuration_templates(
        self,
        replicationConfigurationTemplateIDs: List[str],
        maxResults: int = None,
        nextToken: str = None,
    ) -> DescribeReplicationConfigurationTemplatesResponseTypeDef:
        """
        [Client.describe_replication_configuration_templates documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.describe_replication_configuration_templates)
        """

    def describe_source_servers(
        self,
        filters: DescribeSourceServersRequestFiltersTypeDef,
        maxResults: int = None,
        nextToken: str = None,
    ) -> DescribeSourceServersResponseTypeDef:
        """
        [Client.describe_source_servers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.describe_source_servers)
        """

    def disconnect_from_service(self, sourceServerID: str) -> "SourceServerTypeDef":
        """
        [Client.disconnect_from_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.disconnect_from_service)
        """

    def finalize_cutover(self, sourceServerID: str) -> "SourceServerTypeDef":
        """
        [Client.finalize_cutover documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.finalize_cutover)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.generate_presigned_url)
        """

    def get_launch_configuration(self, sourceServerID: str) -> LaunchConfigurationTypeDef:
        """
        [Client.get_launch_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.get_launch_configuration)
        """

    def get_replication_configuration(self, sourceServerID: str) -> ReplicationConfigurationTypeDef:
        """
        [Client.get_replication_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.get_replication_configuration)
        """

    def initialize_service(self) -> Dict[str, Any]:
        """
        [Client.initialize_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.initialize_service)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.list_tags_for_resource)
        """

    def mark_as_archived(self, sourceServerID: str) -> "SourceServerTypeDef":
        """
        [Client.mark_as_archived documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.mark_as_archived)
        """

    def retry_data_replication(self, sourceServerID: str) -> "SourceServerTypeDef":
        """
        [Client.retry_data_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.retry_data_replication)
        """

    def start_cutover(
        self, sourceServerIDs: List[str], tags: Dict[str, str] = None
    ) -> StartCutoverResponseTypeDef:
        """
        [Client.start_cutover documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.start_cutover)
        """

    def start_test(
        self, sourceServerIDs: List[str], tags: Dict[str, str] = None
    ) -> StartTestResponseTypeDef:
        """
        [Client.start_test documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.start_test)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.tag_resource)
        """

    def terminate_target_instances(
        self, sourceServerIDs: List[str], tags: Dict[str, str] = None
    ) -> TerminateTargetInstancesResponseTypeDef:
        """
        [Client.terminate_target_instances documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.terminate_target_instances)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.untag_resource)
        """

    def update_launch_configuration(
        self,
        sourceServerID: str,
        copyPrivateIp: bool = None,
        copyTags: bool = None,
        launchDisposition: Literal["STOPPED", "STARTED"] = None,
        licensing: "LicensingTypeDef" = None,
        name: str = None,
        targetInstanceTypeRightSizingMethod: Literal["NONE", "BASIC"] = None,
    ) -> LaunchConfigurationTypeDef:
        """
        [Client.update_launch_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.update_launch_configuration)
        """

    def update_replication_configuration(
        self,
        sourceServerID: str,
        associateDefaultSecurityGroup: bool = None,
        bandwidthThrottling: int = None,
        createPublicIP: bool = None,
        dataPlaneRouting: Literal["PRIVATE_IP", "PUBLIC_IP"] = None,
        defaultLargeStagingDiskType: Literal["GP2", "ST1"] = None,
        ebsEncryption: Literal["NONE", "DEFAULT", "CUSTOM"] = None,
        ebsEncryptionKeyArn: str = None,
        name: str = None,
        replicatedDisks: List["ReplicationConfigurationReplicatedDiskTypeDef"] = None,
        replicationServerInstanceType: str = None,
        replicationServersSecurityGroupsIDs: List[str] = None,
        stagingAreaSubnetId: str = None,
        stagingAreaTags: Dict[str, str] = None,
        useDedicatedReplicationServer: bool = None,
    ) -> ReplicationConfigurationTypeDef:
        """
        [Client.update_replication_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.update_replication_configuration)
        """

    def update_replication_configuration_template(
        self,
        replicationConfigurationTemplateID: str,
        arn: str = None,
        associateDefaultSecurityGroup: bool = None,
        bandwidthThrottling: int = None,
        createPublicIP: bool = None,
        dataPlaneRouting: Literal["PRIVATE_IP", "PUBLIC_IP"] = None,
        defaultLargeStagingDiskType: Literal["GP2", "ST1"] = None,
        ebsEncryption: Literal["NONE", "DEFAULT", "CUSTOM"] = None,
        ebsEncryptionKeyArn: str = None,
        replicationServerInstanceType: str = None,
        replicationServersSecurityGroupsIDs: List[str] = None,
        stagingAreaSubnetId: str = None,
        stagingAreaTags: Dict[str, str] = None,
        useDedicatedReplicationServer: bool = None,
    ) -> "ReplicationConfigurationTemplateTypeDef":
        """
        [Client.update_replication_configuration_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Client.update_replication_configuration_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_log_items"]
    ) -> DescribeJobLogItemsPaginator:
        """
        [Paginator.DescribeJobLogItems documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobLogItems)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_jobs"]) -> DescribeJobsPaginator:
        """
        [Paginator.DescribeJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeJobs)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_configuration_templates"]
    ) -> DescribeReplicationConfigurationTemplatesPaginator:
        """
        [Paginator.DescribeReplicationConfigurationTemplates documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeReplicationConfigurationTemplates)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_source_servers"]
    ) -> DescribeSourceServersPaginator:
        """
        [Paginator.DescribeSourceServers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/mgn.html#mgn.Paginator.DescribeSourceServers)
        """
