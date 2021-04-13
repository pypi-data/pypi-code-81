"""
Main interface for accessanalyzer service client

Usage::

    ```python
    import boto3
    from mypy_boto3_accessanalyzer import AccessAnalyzerClient

    client: AccessAnalyzerClient = boto3.client("accessanalyzer")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_accessanalyzer.paginator import (
    ListAccessPreviewFindingsPaginator,
    ListAccessPreviewsPaginator,
    ListAnalyzedResourcesPaginator,
    ListAnalyzersPaginator,
    ListArchiveRulesPaginator,
    ListFindingsPaginator,
    ListPolicyGenerationsPaginator,
    ValidatePolicyPaginator,
)
from mypy_boto3_accessanalyzer.type_defs import (
    CloudTrailDetailsTypeDef,
    ConfigurationTypeDef,
    CreateAccessPreviewResponseTypeDef,
    CreateAnalyzerResponseTypeDef,
    CriterionTypeDef,
    GetAccessPreviewResponseTypeDef,
    GetAnalyzedResourceResponseTypeDef,
    GetAnalyzerResponseTypeDef,
    GetArchiveRuleResponseTypeDef,
    GetFindingResponseTypeDef,
    GetGeneratedPolicyResponseTypeDef,
    InlineArchiveRuleTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PolicyGenerationDetailsTypeDef,
    SortCriteriaTypeDef,
    StartPolicyGenerationResponseTypeDef,
    ValidatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AccessAnalyzerClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AccessAnalyzerClient:
    """
    [AccessAnalyzer.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def apply_archive_rule(self, analyzerArn: str, ruleName: str, clientToken: str = None) -> None:
        """
        [Client.apply_archive_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.apply_archive_rule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.can_paginate)
        """

    def cancel_policy_generation(self, jobId: str) -> Dict[str, Any]:
        """
        [Client.cancel_policy_generation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.cancel_policy_generation)
        """

    def create_access_preview(
        self,
        analyzerArn: str,
        configurations: Dict[str, "ConfigurationTypeDef"],
        clientToken: str = None,
    ) -> CreateAccessPreviewResponseTypeDef:
        """
        [Client.create_access_preview documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_access_preview)
        """

    def create_analyzer(
        self,
        analyzerName: str,
        type: Literal["ACCOUNT", "ORGANIZATION"],
        archiveRules: List[InlineArchiveRuleTypeDef] = None,
        clientToken: str = None,
        tags: Dict[str, str] = None,
    ) -> CreateAnalyzerResponseTypeDef:
        """
        [Client.create_analyzer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_analyzer)
        """

    def create_archive_rule(
        self,
        analyzerName: str,
        filter: Dict[str, "CriterionTypeDef"],
        ruleName: str,
        clientToken: str = None,
    ) -> None:
        """
        [Client.create_archive_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.create_archive_rule)
        """

    def delete_analyzer(self, analyzerName: str, clientToken: str = None) -> None:
        """
        [Client.delete_analyzer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.delete_analyzer)
        """

    def delete_archive_rule(
        self, analyzerName: str, ruleName: str, clientToken: str = None
    ) -> None:
        """
        [Client.delete_archive_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.delete_archive_rule)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.generate_presigned_url)
        """

    def get_access_preview(
        self, accessPreviewId: str, analyzerArn: str
    ) -> GetAccessPreviewResponseTypeDef:
        """
        [Client.get_access_preview documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_access_preview)
        """

    def get_analyzed_resource(
        self, analyzerArn: str, resourceArn: str
    ) -> GetAnalyzedResourceResponseTypeDef:
        """
        [Client.get_analyzed_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_analyzed_resource)
        """

    def get_analyzer(self, analyzerName: str) -> GetAnalyzerResponseTypeDef:
        """
        [Client.get_analyzer documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_analyzer)
        """

    def get_archive_rule(self, analyzerName: str, ruleName: str) -> GetArchiveRuleResponseTypeDef:
        """
        [Client.get_archive_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_archive_rule)
        """

    def get_finding(self, analyzerArn: str, id: str) -> GetFindingResponseTypeDef:
        """
        [Client.get_finding documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_finding)
        """

    def get_generated_policy(
        self,
        jobId: str,
        includeResourcePlaceholders: bool = None,
        includeServiceLevelTemplate: bool = None,
    ) -> GetGeneratedPolicyResponseTypeDef:
        """
        [Client.get_generated_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.get_generated_policy)
        """

    def list_access_preview_findings(
        self,
        accessPreviewId: str,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListAccessPreviewFindingsResponseTypeDef:
        """
        [Client.list_access_preview_findings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_access_preview_findings)
        """

    def list_access_previews(
        self, analyzerArn: str, maxResults: int = None, nextToken: str = None
    ) -> ListAccessPreviewsResponseTypeDef:
        """
        [Client.list_access_previews documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_access_previews)
        """

    def list_analyzed_resources(
        self,
        analyzerArn: str,
        maxResults: int = None,
        nextToken: str = None,
        resourceType: Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ] = None,
    ) -> ListAnalyzedResourcesResponseTypeDef:
        """
        [Client.list_analyzed_resources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_analyzed_resources)
        """

    def list_analyzers(
        self,
        maxResults: int = None,
        nextToken: str = None,
        type: Literal["ACCOUNT", "ORGANIZATION"] = None,
    ) -> ListAnalyzersResponseTypeDef:
        """
        [Client.list_analyzers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_analyzers)
        """

    def list_archive_rules(
        self, analyzerName: str, maxResults: int = None, nextToken: str = None
    ) -> ListArchiveRulesResponseTypeDef:
        """
        [Client.list_archive_rules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_archive_rules)
        """

    def list_findings(
        self,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        maxResults: int = None,
        nextToken: str = None,
        sort: SortCriteriaTypeDef = None,
    ) -> ListFindingsResponseTypeDef:
        """
        [Client.list_findings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_findings)
        """

    def list_policy_generations(
        self, maxResults: int = None, nextToken: str = None, principalArn: str = None
    ) -> ListPolicyGenerationsResponseTypeDef:
        """
        [Client.list_policy_generations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_policy_generations)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.list_tags_for_resource)
        """

    def start_policy_generation(
        self,
        policyGenerationDetails: PolicyGenerationDetailsTypeDef,
        clientToken: str = None,
        cloudTrailDetails: CloudTrailDetailsTypeDef = None,
    ) -> StartPolicyGenerationResponseTypeDef:
        """
        [Client.start_policy_generation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.start_policy_generation)
        """

    def start_resource_scan(self, analyzerArn: str, resourceArn: str) -> None:
        """
        [Client.start_resource_scan documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.start_resource_scan)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.untag_resource)
        """

    def update_archive_rule(
        self,
        analyzerName: str,
        filter: Dict[str, "CriterionTypeDef"],
        ruleName: str,
        clientToken: str = None,
    ) -> None:
        """
        [Client.update_archive_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.update_archive_rule)
        """

    def update_findings(
        self,
        analyzerArn: str,
        status: Literal["ACTIVE", "ARCHIVED"],
        clientToken: str = None,
        ids: List[str] = None,
        resourceArn: str = None,
    ) -> None:
        """
        [Client.update_findings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.update_findings)
        """

    def validate_policy(
        self,
        policyDocument: str,
        policyType: Literal["IDENTITY_POLICY", "RESOURCE_POLICY", "SERVICE_CONTROL_POLICY"],
        locale: Literal["DE", "EN", "ES", "FR", "IT", "JA", "KO", "PT_BR", "ZH_CN", "ZH_TW"] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ValidatePolicyResponseTypeDef:
        """
        [Client.validate_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Client.validate_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_preview_findings"]
    ) -> ListAccessPreviewFindingsPaginator:
        """
        [Paginator.ListAccessPreviewFindings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_previews"]
    ) -> ListAccessPreviewsPaginator:
        """
        [Paginator.ListAccessPreviews documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_analyzed_resources"]
    ) -> ListAnalyzedResourcesPaginator:
        """
        [Paginator.ListAnalyzedResources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_analyzers"]) -> ListAnalyzersPaginator:
        """
        [Paginator.ListAnalyzers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_archive_rules"]
    ) -> ListArchiveRulesPaginator:
        """
        [Paginator.ListArchiveRules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Paginator.ListFindings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_generations"]
    ) -> ListPolicyGenerationsPaginator:
        """
        [Paginator.ListPolicyGenerations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations)
        """

    @overload
    def get_paginator(self, operation_name: Literal["validate_policy"]) -> ValidatePolicyPaginator:
        """
        [Paginator.ValidatePolicy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy)
        """
