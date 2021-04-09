"""
Main interface for accessanalyzer service type definitions.

Usage::

    ```python
    from mypy_boto3_accessanalyzer.type_defs import AccessPreviewFindingTypeDef

    data: AccessPreviewFindingTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessPreviewFindingTypeDef",
    "AccessPreviewStatusReasonTypeDef",
    "AccessPreviewSummaryTypeDef",
    "AccessPreviewTypeDef",
    "AclGranteeTypeDef",
    "AnalyzedResourceSummaryTypeDef",
    "AnalyzedResourceTypeDef",
    "AnalyzerSummaryTypeDef",
    "ArchiveRuleSummaryTypeDef",
    "CloudTrailPropertiesTypeDef",
    "ConfigurationTypeDef",
    "CriterionTypeDef",
    "FindingSourceDetailTypeDef",
    "FindingSourceTypeDef",
    "FindingSummaryTypeDef",
    "FindingTypeDef",
    "GeneratedPolicyPropertiesTypeDef",
    "GeneratedPolicyResultTypeDef",
    "GeneratedPolicyTypeDef",
    "IamRoleConfigurationTypeDef",
    "JobDetailsTypeDef",
    "JobErrorTypeDef",
    "KmsGrantConfigurationTypeDef",
    "KmsGrantConstraintsTypeDef",
    "KmsKeyConfigurationTypeDef",
    "LocationTypeDef",
    "NetworkOriginConfigurationTypeDef",
    "PathElementTypeDef",
    "PolicyGenerationTypeDef",
    "PositionTypeDef",
    "S3AccessPointConfigurationTypeDef",
    "S3BucketAclGrantConfigurationTypeDef",
    "S3BucketConfigurationTypeDef",
    "S3PublicAccessBlockConfigurationTypeDef",
    "SecretsManagerSecretConfigurationTypeDef",
    "SpanTypeDef",
    "SqsQueueConfigurationTypeDef",
    "StatusReasonTypeDef",
    "SubstringTypeDef",
    "TrailPropertiesTypeDef",
    "TrailTypeDef",
    "ValidatePolicyFindingTypeDef",
    "VpcConfigurationTypeDef",
    "CloudTrailDetailsTypeDef",
    "CreateAccessPreviewResponseTypeDef",
    "CreateAnalyzerResponseTypeDef",
    "GetAccessPreviewResponseTypeDef",
    "GetAnalyzedResourceResponseTypeDef",
    "GetAnalyzerResponseTypeDef",
    "GetArchiveRuleResponseTypeDef",
    "GetFindingResponseTypeDef",
    "GetGeneratedPolicyResponseTypeDef",
    "InlineArchiveRuleTypeDef",
    "ListAccessPreviewFindingsResponseTypeDef",
    "ListAccessPreviewsResponseTypeDef",
    "ListAnalyzedResourcesResponseTypeDef",
    "ListAnalyzersResponseTypeDef",
    "ListArchiveRulesResponseTypeDef",
    "ListFindingsResponseTypeDef",
    "ListPolicyGenerationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyGenerationDetailsTypeDef",
    "SortCriteriaTypeDef",
    "StartPolicyGenerationResponseTypeDef",
    "ValidatePolicyResponseTypeDef",
)

_RequiredAccessPreviewFindingTypeDef = TypedDict(
    "_RequiredAccessPreviewFindingTypeDef",
    {
        "changeType": Literal["CHANGED", "NEW", "UNCHANGED"],
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ],
        "status": Literal["ACTIVE", "ARCHIVED", "RESOLVED"],
    },
)
_OptionalAccessPreviewFindingTypeDef = TypedDict(
    "_OptionalAccessPreviewFindingTypeDef",
    {
        "action": List[str],
        "condition": Dict[str, str],
        "error": str,
        "existingFindingId": str,
        "existingFindingStatus": Literal["ACTIVE", "ARCHIVED", "RESOLVED"],
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List["FindingSourceTypeDef"],
    },
    total=False,
)


class AccessPreviewFindingTypeDef(
    _RequiredAccessPreviewFindingTypeDef, _OptionalAccessPreviewFindingTypeDef
):
    pass


AccessPreviewStatusReasonTypeDef = TypedDict(
    "AccessPreviewStatusReasonTypeDef", {"code": Literal["INTERNAL_ERROR", "INVALID_CONFIGURATION"]}
)

_RequiredAccessPreviewSummaryTypeDef = TypedDict(
    "_RequiredAccessPreviewSummaryTypeDef",
    {
        "analyzerArn": str,
        "createdAt": datetime,
        "id": str,
        "status": Literal["COMPLETED", "CREATING", "FAILED"],
    },
)
_OptionalAccessPreviewSummaryTypeDef = TypedDict(
    "_OptionalAccessPreviewSummaryTypeDef",
    {"statusReason": "AccessPreviewStatusReasonTypeDef"},
    total=False,
)


class AccessPreviewSummaryTypeDef(
    _RequiredAccessPreviewSummaryTypeDef, _OptionalAccessPreviewSummaryTypeDef
):
    pass


_RequiredAccessPreviewTypeDef = TypedDict(
    "_RequiredAccessPreviewTypeDef",
    {
        "analyzerArn": str,
        "configurations": Dict[str, "ConfigurationTypeDef"],
        "createdAt": datetime,
        "id": str,
        "status": Literal["COMPLETED", "CREATING", "FAILED"],
    },
)
_OptionalAccessPreviewTypeDef = TypedDict(
    "_OptionalAccessPreviewTypeDef",
    {"statusReason": "AccessPreviewStatusReasonTypeDef"},
    total=False,
)


class AccessPreviewTypeDef(_RequiredAccessPreviewTypeDef, _OptionalAccessPreviewTypeDef):
    pass


AclGranteeTypeDef = TypedDict("AclGranteeTypeDef", {"id": str, "uri": str}, total=False)

AnalyzedResourceSummaryTypeDef = TypedDict(
    "AnalyzedResourceSummaryTypeDef",
    {
        "resourceArn": str,
        "resourceOwnerAccount": str,
        "resourceType": Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ],
    },
)

_RequiredAnalyzedResourceTypeDef = TypedDict(
    "_RequiredAnalyzedResourceTypeDef",
    {
        "analyzedAt": datetime,
        "createdAt": datetime,
        "isPublic": bool,
        "resourceArn": str,
        "resourceOwnerAccount": str,
        "resourceType": Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ],
        "updatedAt": datetime,
    },
)
_OptionalAnalyzedResourceTypeDef = TypedDict(
    "_OptionalAnalyzedResourceTypeDef",
    {
        "actions": List[str],
        "error": str,
        "sharedVia": List[str],
        "status": Literal["ACTIVE", "ARCHIVED", "RESOLVED"],
    },
    total=False,
)


class AnalyzedResourceTypeDef(_RequiredAnalyzedResourceTypeDef, _OptionalAnalyzedResourceTypeDef):
    pass


_RequiredAnalyzerSummaryTypeDef = TypedDict(
    "_RequiredAnalyzerSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "name": str,
        "status": Literal["ACTIVE", "CREATING", "DISABLED", "FAILED"],
        "type": Literal["ACCOUNT", "ORGANIZATION"],
    },
)
_OptionalAnalyzerSummaryTypeDef = TypedDict(
    "_OptionalAnalyzerSummaryTypeDef",
    {
        "lastResourceAnalyzed": str,
        "lastResourceAnalyzedAt": datetime,
        "statusReason": "StatusReasonTypeDef",
        "tags": Dict[str, str],
    },
    total=False,
)


class AnalyzerSummaryTypeDef(_RequiredAnalyzerSummaryTypeDef, _OptionalAnalyzerSummaryTypeDef):
    pass


ArchiveRuleSummaryTypeDef = TypedDict(
    "ArchiveRuleSummaryTypeDef",
    {
        "createdAt": datetime,
        "filter": Dict[str, "CriterionTypeDef"],
        "ruleName": str,
        "updatedAt": datetime,
    },
)

CloudTrailPropertiesTypeDef = TypedDict(
    "CloudTrailPropertiesTypeDef",
    {"endTime": datetime, "startTime": datetime, "trailProperties": List["TrailPropertiesTypeDef"]},
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "iamRole": "IamRoleConfigurationTypeDef",
        "kmsKey": "KmsKeyConfigurationTypeDef",
        "s3Bucket": "S3BucketConfigurationTypeDef",
        "secretsManagerSecret": "SecretsManagerSecretConfigurationTypeDef",
        "sqsQueue": "SqsQueueConfigurationTypeDef",
    },
    total=False,
)

CriterionTypeDef = TypedDict(
    "CriterionTypeDef",
    {"contains": List[str], "eq": List[str], "exists": bool, "neq": List[str]},
    total=False,
)

FindingSourceDetailTypeDef = TypedDict(
    "FindingSourceDetailTypeDef", {"accessPointArn": str}, total=False
)

_RequiredFindingSourceTypeDef = TypedDict(
    "_RequiredFindingSourceTypeDef", {"type": Literal["POLICY", "BUCKET_ACL", "S3_ACCESS_POINT"]}
)
_OptionalFindingSourceTypeDef = TypedDict(
    "_OptionalFindingSourceTypeDef", {"detail": "FindingSourceDetailTypeDef"}, total=False
)


class FindingSourceTypeDef(_RequiredFindingSourceTypeDef, _OptionalFindingSourceTypeDef):
    pass


_RequiredFindingSummaryTypeDef = TypedDict(
    "_RequiredFindingSummaryTypeDef",
    {
        "analyzedAt": datetime,
        "condition": Dict[str, str],
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ],
        "status": Literal["ACTIVE", "ARCHIVED", "RESOLVED"],
        "updatedAt": datetime,
    },
)
_OptionalFindingSummaryTypeDef = TypedDict(
    "_OptionalFindingSummaryTypeDef",
    {
        "action": List[str],
        "error": str,
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List["FindingSourceTypeDef"],
    },
    total=False,
)


class FindingSummaryTypeDef(_RequiredFindingSummaryTypeDef, _OptionalFindingSummaryTypeDef):
    pass


_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "analyzedAt": datetime,
        "condition": Dict[str, str],
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": Literal[
            "AWS::S3::Bucket",
            "AWS::IAM::Role",
            "AWS::SQS::Queue",
            "AWS::Lambda::Function",
            "AWS::Lambda::LayerVersion",
            "AWS::KMS::Key",
            "AWS::SecretsManager::Secret",
        ],
        "status": Literal["ACTIVE", "ARCHIVED", "RESOLVED"],
        "updatedAt": datetime,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "action": List[str],
        "error": str,
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List["FindingSourceTypeDef"],
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


_RequiredGeneratedPolicyPropertiesTypeDef = TypedDict(
    "_RequiredGeneratedPolicyPropertiesTypeDef", {"principalArn": str}
)
_OptionalGeneratedPolicyPropertiesTypeDef = TypedDict(
    "_OptionalGeneratedPolicyPropertiesTypeDef",
    {"cloudTrailProperties": "CloudTrailPropertiesTypeDef", "isComplete": bool},
    total=False,
)


class GeneratedPolicyPropertiesTypeDef(
    _RequiredGeneratedPolicyPropertiesTypeDef, _OptionalGeneratedPolicyPropertiesTypeDef
):
    pass


_RequiredGeneratedPolicyResultTypeDef = TypedDict(
    "_RequiredGeneratedPolicyResultTypeDef", {"properties": "GeneratedPolicyPropertiesTypeDef"}
)
_OptionalGeneratedPolicyResultTypeDef = TypedDict(
    "_OptionalGeneratedPolicyResultTypeDef",
    {"generatedPolicies": List["GeneratedPolicyTypeDef"]},
    total=False,
)


class GeneratedPolicyResultTypeDef(
    _RequiredGeneratedPolicyResultTypeDef, _OptionalGeneratedPolicyResultTypeDef
):
    pass


GeneratedPolicyTypeDef = TypedDict("GeneratedPolicyTypeDef", {"policy": str})

IamRoleConfigurationTypeDef = TypedDict(
    "IamRoleConfigurationTypeDef", {"trustPolicy": str}, total=False
)

_RequiredJobDetailsTypeDef = TypedDict(
    "_RequiredJobDetailsTypeDef",
    {
        "jobId": str,
        "startedOn": datetime,
        "status": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED", "CANCELED"],
    },
)
_OptionalJobDetailsTypeDef = TypedDict(
    "_OptionalJobDetailsTypeDef",
    {"completedOn": datetime, "jobError": "JobErrorTypeDef"},
    total=False,
)


class JobDetailsTypeDef(_RequiredJobDetailsTypeDef, _OptionalJobDetailsTypeDef):
    pass


JobErrorTypeDef = TypedDict(
    "JobErrorTypeDef",
    {
        "code": Literal[
            "AUTHORIZATION_ERROR",
            "RESOURCE_NOT_FOUND_ERROR",
            "SERVICE_QUOTA_EXCEEDED_ERROR",
            "SERVICE_ERROR",
        ],
        "message": str,
    },
)

_RequiredKmsGrantConfigurationTypeDef = TypedDict(
    "_RequiredKmsGrantConfigurationTypeDef",
    {
        "granteePrincipal": str,
        "issuingAccount": str,
        "operations": List[
            Literal[
                "CreateGrant",
                "Decrypt",
                "DescribeKey",
                "Encrypt",
                "GenerateDataKey",
                "GenerateDataKeyPair",
                "GenerateDataKeyPairWithoutPlaintext",
                "GenerateDataKeyWithoutPlaintext",
                "GetPublicKey",
                "ReEncryptFrom",
                "ReEncryptTo",
                "RetireGrant",
                "Sign",
                "Verify",
            ]
        ],
    },
)
_OptionalKmsGrantConfigurationTypeDef = TypedDict(
    "_OptionalKmsGrantConfigurationTypeDef",
    {"constraints": "KmsGrantConstraintsTypeDef", "retiringPrincipal": str},
    total=False,
)


class KmsGrantConfigurationTypeDef(
    _RequiredKmsGrantConfigurationTypeDef, _OptionalKmsGrantConfigurationTypeDef
):
    pass


KmsGrantConstraintsTypeDef = TypedDict(
    "KmsGrantConstraintsTypeDef",
    {"encryptionContextEquals": Dict[str, str], "encryptionContextSubset": Dict[str, str]},
    total=False,
)

KmsKeyConfigurationTypeDef = TypedDict(
    "KmsKeyConfigurationTypeDef",
    {"grants": List["KmsGrantConfigurationTypeDef"], "keyPolicies": Dict[str, str]},
    total=False,
)

LocationTypeDef = TypedDict(
    "LocationTypeDef", {"path": List["PathElementTypeDef"], "span": "SpanTypeDef"}
)

NetworkOriginConfigurationTypeDef = TypedDict(
    "NetworkOriginConfigurationTypeDef",
    {"internetConfiguration": Dict[str, Any], "vpcConfiguration": "VpcConfigurationTypeDef"},
    total=False,
)

PathElementTypeDef = TypedDict(
    "PathElementTypeDef",
    {"index": int, "key": str, "substring": "SubstringTypeDef", "value": str},
    total=False,
)

_RequiredPolicyGenerationTypeDef = TypedDict(
    "_RequiredPolicyGenerationTypeDef",
    {
        "jobId": str,
        "principalArn": str,
        "startedOn": datetime,
        "status": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED", "CANCELED"],
    },
)
_OptionalPolicyGenerationTypeDef = TypedDict(
    "_OptionalPolicyGenerationTypeDef", {"completedOn": datetime}, total=False
)


class PolicyGenerationTypeDef(_RequiredPolicyGenerationTypeDef, _OptionalPolicyGenerationTypeDef):
    pass


PositionTypeDef = TypedDict("PositionTypeDef", {"column": int, "line": int, "offset": int})

S3AccessPointConfigurationTypeDef = TypedDict(
    "S3AccessPointConfigurationTypeDef",
    {
        "accessPointPolicy": str,
        "networkOrigin": "NetworkOriginConfigurationTypeDef",
        "publicAccessBlock": "S3PublicAccessBlockConfigurationTypeDef",
    },
    total=False,
)

S3BucketAclGrantConfigurationTypeDef = TypedDict(
    "S3BucketAclGrantConfigurationTypeDef",
    {
        "grantee": "AclGranteeTypeDef",
        "permission": Literal["READ", "WRITE", "READ_ACP", "WRITE_ACP", "FULL_CONTROL"],
    },
)

S3BucketConfigurationTypeDef = TypedDict(
    "S3BucketConfigurationTypeDef",
    {
        "accessPoints": Dict[str, "S3AccessPointConfigurationTypeDef"],
        "bucketAclGrants": List["S3BucketAclGrantConfigurationTypeDef"],
        "bucketPolicy": str,
        "bucketPublicAccessBlock": "S3PublicAccessBlockConfigurationTypeDef",
    },
    total=False,
)

S3PublicAccessBlockConfigurationTypeDef = TypedDict(
    "S3PublicAccessBlockConfigurationTypeDef",
    {"ignorePublicAcls": bool, "restrictPublicBuckets": bool},
)

SecretsManagerSecretConfigurationTypeDef = TypedDict(
    "SecretsManagerSecretConfigurationTypeDef", {"kmsKeyId": str, "secretPolicy": str}, total=False
)

SpanTypeDef = TypedDict("SpanTypeDef", {"end": "PositionTypeDef", "start": "PositionTypeDef"})

SqsQueueConfigurationTypeDef = TypedDict(
    "SqsQueueConfigurationTypeDef", {"queuePolicy": str}, total=False
)

StatusReasonTypeDef = TypedDict(
    "StatusReasonTypeDef",
    {
        "code": Literal[
            "AWS_SERVICE_ACCESS_DISABLED",
            "DELEGATED_ADMINISTRATOR_DEREGISTERED",
            "ORGANIZATION_DELETED",
            "SERVICE_LINKED_ROLE_CREATION_FAILED",
        ]
    },
)

SubstringTypeDef = TypedDict("SubstringTypeDef", {"length": int, "start": int})

_RequiredTrailPropertiesTypeDef = TypedDict(
    "_RequiredTrailPropertiesTypeDef", {"cloudTrailArn": str}
)
_OptionalTrailPropertiesTypeDef = TypedDict(
    "_OptionalTrailPropertiesTypeDef", {"allRegions": bool, "regions": List[str]}, total=False
)


class TrailPropertiesTypeDef(_RequiredTrailPropertiesTypeDef, _OptionalTrailPropertiesTypeDef):
    pass


_RequiredTrailTypeDef = TypedDict("_RequiredTrailTypeDef", {"cloudTrailArn": str})
_OptionalTrailTypeDef = TypedDict(
    "_OptionalTrailTypeDef", {"allRegions": bool, "regions": List[str]}, total=False
)


class TrailTypeDef(_RequiredTrailTypeDef, _OptionalTrailTypeDef):
    pass


ValidatePolicyFindingTypeDef = TypedDict(
    "ValidatePolicyFindingTypeDef",
    {
        "findingDetails": str,
        "findingType": Literal["ERROR", "SECURITY_WARNING", "SUGGESTION", "WARNING"],
        "issueCode": str,
        "learnMoreLink": str,
        "locations": List["LocationTypeDef"],
    },
)

VpcConfigurationTypeDef = TypedDict("VpcConfigurationTypeDef", {"vpcId": str})

_RequiredCloudTrailDetailsTypeDef = TypedDict(
    "_RequiredCloudTrailDetailsTypeDef",
    {"accessRole": str, "startTime": datetime, "trails": List["TrailTypeDef"]},
)
_OptionalCloudTrailDetailsTypeDef = TypedDict(
    "_OptionalCloudTrailDetailsTypeDef", {"endTime": datetime}, total=False
)


class CloudTrailDetailsTypeDef(
    _RequiredCloudTrailDetailsTypeDef, _OptionalCloudTrailDetailsTypeDef
):
    pass


CreateAccessPreviewResponseTypeDef = TypedDict("CreateAccessPreviewResponseTypeDef", {"id": str})

CreateAnalyzerResponseTypeDef = TypedDict(
    "CreateAnalyzerResponseTypeDef", {"arn": str}, total=False
)

GetAccessPreviewResponseTypeDef = TypedDict(
    "GetAccessPreviewResponseTypeDef", {"accessPreview": "AccessPreviewTypeDef"}
)

GetAnalyzedResourceResponseTypeDef = TypedDict(
    "GetAnalyzedResourceResponseTypeDef", {"resource": "AnalyzedResourceTypeDef"}, total=False
)

GetAnalyzerResponseTypeDef = TypedDict(
    "GetAnalyzerResponseTypeDef", {"analyzer": "AnalyzerSummaryTypeDef"}
)

GetArchiveRuleResponseTypeDef = TypedDict(
    "GetArchiveRuleResponseTypeDef", {"archiveRule": "ArchiveRuleSummaryTypeDef"}
)

GetFindingResponseTypeDef = TypedDict(
    "GetFindingResponseTypeDef", {"finding": "FindingTypeDef"}, total=False
)

GetGeneratedPolicyResponseTypeDef = TypedDict(
    "GetGeneratedPolicyResponseTypeDef",
    {"generatedPolicyResult": "GeneratedPolicyResultTypeDef", "jobDetails": "JobDetailsTypeDef"},
)

InlineArchiveRuleTypeDef = TypedDict(
    "InlineArchiveRuleTypeDef", {"filter": Dict[str, "CriterionTypeDef"], "ruleName": str}
)

_RequiredListAccessPreviewFindingsResponseTypeDef = TypedDict(
    "_RequiredListAccessPreviewFindingsResponseTypeDef",
    {"findings": List["AccessPreviewFindingTypeDef"]},
)
_OptionalListAccessPreviewFindingsResponseTypeDef = TypedDict(
    "_OptionalListAccessPreviewFindingsResponseTypeDef", {"nextToken": str}, total=False
)


class ListAccessPreviewFindingsResponseTypeDef(
    _RequiredListAccessPreviewFindingsResponseTypeDef,
    _OptionalListAccessPreviewFindingsResponseTypeDef,
):
    pass


_RequiredListAccessPreviewsResponseTypeDef = TypedDict(
    "_RequiredListAccessPreviewsResponseTypeDef",
    {"accessPreviews": List["AccessPreviewSummaryTypeDef"]},
)
_OptionalListAccessPreviewsResponseTypeDef = TypedDict(
    "_OptionalListAccessPreviewsResponseTypeDef", {"nextToken": str}, total=False
)


class ListAccessPreviewsResponseTypeDef(
    _RequiredListAccessPreviewsResponseTypeDef, _OptionalListAccessPreviewsResponseTypeDef
):
    pass


_RequiredListAnalyzedResourcesResponseTypeDef = TypedDict(
    "_RequiredListAnalyzedResourcesResponseTypeDef",
    {"analyzedResources": List["AnalyzedResourceSummaryTypeDef"]},
)
_OptionalListAnalyzedResourcesResponseTypeDef = TypedDict(
    "_OptionalListAnalyzedResourcesResponseTypeDef", {"nextToken": str}, total=False
)


class ListAnalyzedResourcesResponseTypeDef(
    _RequiredListAnalyzedResourcesResponseTypeDef, _OptionalListAnalyzedResourcesResponseTypeDef
):
    pass


_RequiredListAnalyzersResponseTypeDef = TypedDict(
    "_RequiredListAnalyzersResponseTypeDef", {"analyzers": List["AnalyzerSummaryTypeDef"]}
)
_OptionalListAnalyzersResponseTypeDef = TypedDict(
    "_OptionalListAnalyzersResponseTypeDef", {"nextToken": str}, total=False
)


class ListAnalyzersResponseTypeDef(
    _RequiredListAnalyzersResponseTypeDef, _OptionalListAnalyzersResponseTypeDef
):
    pass


_RequiredListArchiveRulesResponseTypeDef = TypedDict(
    "_RequiredListArchiveRulesResponseTypeDef", {"archiveRules": List["ArchiveRuleSummaryTypeDef"]}
)
_OptionalListArchiveRulesResponseTypeDef = TypedDict(
    "_OptionalListArchiveRulesResponseTypeDef", {"nextToken": str}, total=False
)


class ListArchiveRulesResponseTypeDef(
    _RequiredListArchiveRulesResponseTypeDef, _OptionalListArchiveRulesResponseTypeDef
):
    pass


_RequiredListFindingsResponseTypeDef = TypedDict(
    "_RequiredListFindingsResponseTypeDef", {"findings": List["FindingSummaryTypeDef"]}
)
_OptionalListFindingsResponseTypeDef = TypedDict(
    "_OptionalListFindingsResponseTypeDef", {"nextToken": str}, total=False
)


class ListFindingsResponseTypeDef(
    _RequiredListFindingsResponseTypeDef, _OptionalListFindingsResponseTypeDef
):
    pass


_RequiredListPolicyGenerationsResponseTypeDef = TypedDict(
    "_RequiredListPolicyGenerationsResponseTypeDef",
    {"policyGenerations": List["PolicyGenerationTypeDef"]},
)
_OptionalListPolicyGenerationsResponseTypeDef = TypedDict(
    "_OptionalListPolicyGenerationsResponseTypeDef", {"nextToken": str}, total=False
)


class ListPolicyGenerationsResponseTypeDef(
    _RequiredListPolicyGenerationsResponseTypeDef, _OptionalListPolicyGenerationsResponseTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PolicyGenerationDetailsTypeDef = TypedDict("PolicyGenerationDetailsTypeDef", {"principalArn": str})

SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef", {"attributeName": str, "orderBy": Literal["ASC", "DESC"]}, total=False
)

StartPolicyGenerationResponseTypeDef = TypedDict(
    "StartPolicyGenerationResponseTypeDef", {"jobId": str}
)

_RequiredValidatePolicyResponseTypeDef = TypedDict(
    "_RequiredValidatePolicyResponseTypeDef", {"findings": List["ValidatePolicyFindingTypeDef"]}
)
_OptionalValidatePolicyResponseTypeDef = TypedDict(
    "_OptionalValidatePolicyResponseTypeDef", {"nextToken": str}, total=False
)


class ValidatePolicyResponseTypeDef(
    _RequiredValidatePolicyResponseTypeDef, _OptionalValidatePolicyResponseTypeDef
):
    pass
