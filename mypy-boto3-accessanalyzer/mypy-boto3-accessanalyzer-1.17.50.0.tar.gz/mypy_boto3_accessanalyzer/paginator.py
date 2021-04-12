"""
Main interface for accessanalyzer service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_accessanalyzer import AccessAnalyzerClient
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

    client: AccessAnalyzerClient = boto3.client("accessanalyzer")

    list_access_preview_findings_paginator: ListAccessPreviewFindingsPaginator = client.get_paginator("list_access_preview_findings")
    list_access_previews_paginator: ListAccessPreviewsPaginator = client.get_paginator("list_access_previews")
    list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
    list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
    list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
    validate_policy_paginator: ValidatePolicyPaginator = client.get_paginator("validate_policy")
    ```
"""
import sys
from typing import Dict, Iterator

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_accessanalyzer.type_defs import (
    CriterionTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
    ValidatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAccessPreviewFindingsPaginator",
    "ListAccessPreviewsPaginator",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
    "ListPolicyGenerationsPaginator",
    "ValidatePolicyPaginator",
)


class ListAccessPreviewFindingsPaginator(Boto3Paginator):
    """
    [Paginator.ListAccessPreviewFindings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)
    """

    def paginate(
        self,
        accessPreviewId: str,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAccessPreviewFindingsResponseTypeDef]:
        """
        [ListAccessPreviewFindings.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings.paginate)
        """


class ListAccessPreviewsPaginator(Boto3Paginator):
    """
    [Paginator.ListAccessPreviews documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews)
    """

    def paginate(
        self, analyzerArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccessPreviewsResponseTypeDef]:
        """
        [ListAccessPreviews.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews.paginate)
        """


class ListAnalyzedResourcesPaginator(Boto3Paginator):
    """
    [Paginator.ListAnalyzedResources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources)
    """

    def paginate(
        self,
        analyzerArn: str,
        resourceType: Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAnalyzedResourcesResponseTypeDef]:
        """
        [ListAnalyzedResources.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources.paginate)
        """


class ListAnalyzersPaginator(Boto3Paginator):
    """
    [Paginator.ListAnalyzers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers)
    """

    def paginate(
        self,
        type: Literal["ACCOUNT", "ORGANIZATION"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAnalyzersResponseTypeDef]:
        """
        [ListAnalyzers.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers.paginate)
        """


class ListArchiveRulesPaginator(Boto3Paginator):
    """
    [Paginator.ListArchiveRules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules)
    """

    def paginate(
        self, analyzerName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListArchiveRulesResponseTypeDef]:
        """
        [ListArchiveRules.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules.paginate)
        """


class ListFindingsPaginator(Boto3Paginator):
    """
    [Paginator.ListFindings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings)
    """

    def paginate(
        self,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        sort: SortCriteriaTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListFindingsResponseTypeDef]:
        """
        [ListFindings.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings.paginate)
        """


class ListPolicyGenerationsPaginator(Boto3Paginator):
    """
    [Paginator.ListPolicyGenerations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations)
    """

    def paginate(
        self, principalArn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [ListPolicyGenerations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations.paginate)
        """


class ValidatePolicyPaginator(Boto3Paginator):
    """
    [Paginator.ValidatePolicy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy)
    """

    def paginate(
        self,
        policyDocument: str,
        policyType: Literal["IDENTITY_POLICY", "RESOURCE_POLICY", "SERVICE_CONTROL_POLICY"],
        locale: Literal["DE", "EN", "ES", "FR", "IT", "JA", "KO", "PT_BR", "ZH_CN", "ZH_TW"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ValidatePolicyResponseTypeDef]:
        """
        [ValidatePolicy.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy.paginate)
        """
