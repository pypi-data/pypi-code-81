"""
Main interface for lookoutmetrics service type definitions.

Usage::

    ```python
    from mypy_boto3_lookoutmetrics.type_defs import ActionTypeDef

    data: ActionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActionTypeDef",
    "AlertSummaryTypeDef",
    "AlertTypeDef",
    "AnomalyDetectorConfigSummaryTypeDef",
    "AnomalyDetectorSummaryTypeDef",
    "AnomalyGroupStatisticsTypeDef",
    "AnomalyGroupSummaryTypeDef",
    "AnomalyGroupTypeDef",
    "AppFlowConfigTypeDef",
    "CloudWatchConfigTypeDef",
    "ContributionMatrixTypeDef",
    "CsvFormatDescriptorTypeDef",
    "DimensionContributionTypeDef",
    "DimensionNameValueTypeDef",
    "DimensionValueContributionTypeDef",
    "ExecutionStatusTypeDef",
    "FileFormatDescriptorTypeDef",
    "ItemizedMetricStatsTypeDef",
    "JsonFormatDescriptorTypeDef",
    "LambdaConfigurationTypeDef",
    "MetricLevelImpactTypeDef",
    "MetricSetSummaryTypeDef",
    "MetricSourceTypeDef",
    "MetricTypeDef",
    "RDSSourceConfigTypeDef",
    "RedshiftSourceConfigTypeDef",
    "S3SourceConfigTypeDef",
    "SNSConfigurationTypeDef",
    "TimeSeriesFeedbackTypeDef",
    "TimeSeriesTypeDef",
    "TimestampColumnTypeDef",
    "VpcConfigurationTypeDef",
    "AnomalyDetectorConfigTypeDef",
    "AnomalyGroupTimeSeriesFeedbackTypeDef",
    "AnomalyGroupTimeSeriesTypeDef",
    "CreateAlertResponseTypeDef",
    "CreateAnomalyDetectorResponseTypeDef",
    "CreateMetricSetResponseTypeDef",
    "DescribeAlertResponseTypeDef",
    "DescribeAnomalyDetectionExecutionsResponseTypeDef",
    "DescribeAnomalyDetectorResponseTypeDef",
    "DescribeMetricSetResponseTypeDef",
    "GetAnomalyGroupResponseTypeDef",
    "GetFeedbackResponseTypeDef",
    "GetSampleDataResponseTypeDef",
    "ListAlertsResponseTypeDef",
    "ListAnomalyDetectorsResponseTypeDef",
    "ListAnomalyGroupSummariesResponseTypeDef",
    "ListAnomalyGroupTimeSeriesResponseTypeDef",
    "ListMetricSetsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SampleDataS3SourceConfigTypeDef",
    "UpdateAnomalyDetectorResponseTypeDef",
    "UpdateMetricSetResponseTypeDef",
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "SNSConfiguration": "SNSConfigurationTypeDef",
        "LambdaConfiguration": "LambdaConfigurationTypeDef",
    },
    total=False,
)

AlertSummaryTypeDef = TypedDict(
    "AlertSummaryTypeDef",
    {
        "AlertArn": str,
        "AnomalyDetectorArn": str,
        "AlertName": str,
        "AlertSensitivityThreshold": int,
        "AlertType": Literal["SNS", "LAMBDA"],
        "AlertStatus": Literal["ACTIVE", "INACTIVE"],
        "LastModificationTime": datetime,
        "CreationTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)

AlertTypeDef = TypedDict(
    "AlertTypeDef",
    {
        "Action": "ActionTypeDef",
        "AlertDescription": str,
        "AlertArn": str,
        "AnomalyDetectorArn": str,
        "AlertName": str,
        "AlertSensitivityThreshold": int,
        "AlertType": Literal["SNS", "LAMBDA"],
        "AlertStatus": Literal["ACTIVE", "INACTIVE"],
        "LastModificationTime": datetime,
        "CreationTime": datetime,
    },
    total=False,
)

AnomalyDetectorConfigSummaryTypeDef = TypedDict(
    "AnomalyDetectorConfigSummaryTypeDef",
    {"AnomalyDetectorFrequency": Literal["P1D", "PT1H", "PT10M", "PT5M"]},
    total=False,
)

AnomalyDetectorSummaryTypeDef = TypedDict(
    "AnomalyDetectorSummaryTypeDef",
    {
        "AnomalyDetectorArn": str,
        "AnomalyDetectorName": str,
        "AnomalyDetectorDescription": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Status": Literal[
            "ACTIVE",
            "ACTIVATING",
            "DELETING",
            "FAILED",
            "INACTIVE",
            "BACK_TEST_ACTIVATING",
            "BACK_TEST_ACTIVE",
            "BACK_TEST_COMPLETE",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

AnomalyGroupStatisticsTypeDef = TypedDict(
    "AnomalyGroupStatisticsTypeDef",
    {
        "EvaluationStartDate": str,
        "TotalCount": int,
        "ItemizedMetricStatsList": List["ItemizedMetricStatsTypeDef"],
    },
    total=False,
)

AnomalyGroupSummaryTypeDef = TypedDict(
    "AnomalyGroupSummaryTypeDef",
    {
        "StartTime": str,
        "EndTime": str,
        "AnomalyGroupId": str,
        "AnomalyGroupScore": float,
        "PrimaryMetricName": str,
    },
    total=False,
)

AnomalyGroupTypeDef = TypedDict(
    "AnomalyGroupTypeDef",
    {
        "StartTime": str,
        "EndTime": str,
        "AnomalyGroupId": str,
        "AnomalyGroupScore": float,
        "PrimaryMetricName": str,
        "MetricLevelImpactList": List["MetricLevelImpactTypeDef"],
    },
    total=False,
)

AppFlowConfigTypeDef = TypedDict("AppFlowConfigTypeDef", {"RoleArn": str, "FlowName": str})

CloudWatchConfigTypeDef = TypedDict("CloudWatchConfigTypeDef", {"RoleArn": str})

ContributionMatrixTypeDef = TypedDict(
    "ContributionMatrixTypeDef",
    {"DimensionContributionList": List["DimensionContributionTypeDef"]},
    total=False,
)

CsvFormatDescriptorTypeDef = TypedDict(
    "CsvFormatDescriptorTypeDef",
    {
        "FileCompression": Literal["NONE", "GZIP"],
        "Charset": str,
        "ContainsHeader": bool,
        "Delimiter": str,
        "HeaderList": List[str],
        "QuoteSymbol": str,
    },
    total=False,
)

DimensionContributionTypeDef = TypedDict(
    "DimensionContributionTypeDef",
    {
        "DimensionName": str,
        "DimensionValueContributionList": List["DimensionValueContributionTypeDef"],
    },
    total=False,
)

DimensionNameValueTypeDef = TypedDict(
    "DimensionNameValueTypeDef", {"DimensionName": str, "DimensionValue": str}
)

DimensionValueContributionTypeDef = TypedDict(
    "DimensionValueContributionTypeDef",
    {"DimensionValue": str, "ContributionScore": float},
    total=False,
)

ExecutionStatusTypeDef = TypedDict(
    "ExecutionStatusTypeDef",
    {
        "Timestamp": str,
        "Status": Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "FAILED_TO_SCHEDULE"],
        "FailureReason": str,
    },
    total=False,
)

FileFormatDescriptorTypeDef = TypedDict(
    "FileFormatDescriptorTypeDef",
    {
        "CsvFormatDescriptor": "CsvFormatDescriptorTypeDef",
        "JsonFormatDescriptor": "JsonFormatDescriptorTypeDef",
    },
    total=False,
)

ItemizedMetricStatsTypeDef = TypedDict(
    "ItemizedMetricStatsTypeDef", {"MetricName": str, "OccurrenceCount": int}, total=False
)

JsonFormatDescriptorTypeDef = TypedDict(
    "JsonFormatDescriptorTypeDef",
    {"FileCompression": Literal["NONE", "GZIP"], "Charset": str},
    total=False,
)

LambdaConfigurationTypeDef = TypedDict(
    "LambdaConfigurationTypeDef", {"RoleArn": str, "LambdaArn": str}
)

MetricLevelImpactTypeDef = TypedDict(
    "MetricLevelImpactTypeDef",
    {"MetricName": str, "NumTimeSeries": int, "ContributionMatrix": "ContributionMatrixTypeDef"},
    total=False,
)

MetricSetSummaryTypeDef = TypedDict(
    "MetricSetSummaryTypeDef",
    {
        "MetricSetArn": str,
        "AnomalyDetectorArn": str,
        "MetricSetDescription": str,
        "MetricSetName": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Tags": Dict[str, str],
    },
    total=False,
)

MetricSourceTypeDef = TypedDict(
    "MetricSourceTypeDef",
    {
        "S3SourceConfig": "S3SourceConfigTypeDef",
        "AppFlowConfig": "AppFlowConfigTypeDef",
        "CloudWatchConfig": "CloudWatchConfigTypeDef",
        "RDSSourceConfig": "RDSSourceConfigTypeDef",
        "RedshiftSourceConfig": "RedshiftSourceConfigTypeDef",
    },
    total=False,
)

_RequiredMetricTypeDef = TypedDict(
    "_RequiredMetricTypeDef", {"MetricName": str, "AggregationFunction": Literal["AVG", "SUM"]}
)
_OptionalMetricTypeDef = TypedDict("_OptionalMetricTypeDef", {"Namespace": str}, total=False)


class MetricTypeDef(_RequiredMetricTypeDef, _OptionalMetricTypeDef):
    pass


RDSSourceConfigTypeDef = TypedDict(
    "RDSSourceConfigTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DatabaseHost": str,
        "DatabasePort": int,
        "SecretManagerArn": str,
        "DatabaseName": str,
        "TableName": str,
        "RoleArn": str,
        "VpcConfiguration": "VpcConfigurationTypeDef",
    },
)

RedshiftSourceConfigTypeDef = TypedDict(
    "RedshiftSourceConfigTypeDef",
    {
        "ClusterIdentifier": str,
        "DatabaseHost": str,
        "DatabasePort": int,
        "SecretManagerArn": str,
        "DatabaseName": str,
        "TableName": str,
        "RoleArn": str,
        "VpcConfiguration": "VpcConfigurationTypeDef",
    },
)

_RequiredS3SourceConfigTypeDef = TypedDict("_RequiredS3SourceConfigTypeDef", {"RoleArn": str})
_OptionalS3SourceConfigTypeDef = TypedDict(
    "_OptionalS3SourceConfigTypeDef",
    {
        "TemplatedPathList": List[str],
        "HistoricalDataPathList": List[str],
        "FileFormatDescriptor": "FileFormatDescriptorTypeDef",
    },
    total=False,
)


class S3SourceConfigTypeDef(_RequiredS3SourceConfigTypeDef, _OptionalS3SourceConfigTypeDef):
    pass


SNSConfigurationTypeDef = TypedDict("SNSConfigurationTypeDef", {"RoleArn": str, "SnsTopicArn": str})

TimeSeriesFeedbackTypeDef = TypedDict(
    "TimeSeriesFeedbackTypeDef", {"TimeSeriesId": str, "IsAnomaly": bool}, total=False
)

TimeSeriesTypeDef = TypedDict(
    "TimeSeriesTypeDef",
    {
        "TimeSeriesId": str,
        "DimensionList": List["DimensionNameValueTypeDef"],
        "MetricValueList": List[float],
    },
)

TimestampColumnTypeDef = TypedDict(
    "TimestampColumnTypeDef", {"ColumnName": str, "ColumnFormat": str}, total=False
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef", {"SubnetIdList": List[str], "SecurityGroupIdList": List[str]}
)

AnomalyDetectorConfigTypeDef = TypedDict(
    "AnomalyDetectorConfigTypeDef",
    {"AnomalyDetectorFrequency": Literal["P1D", "PT1H", "PT10M", "PT5M"]},
    total=False,
)

AnomalyGroupTimeSeriesFeedbackTypeDef = TypedDict(
    "AnomalyGroupTimeSeriesFeedbackTypeDef",
    {"AnomalyGroupId": str, "TimeSeriesId": str, "IsAnomaly": bool},
)

_RequiredAnomalyGroupTimeSeriesTypeDef = TypedDict(
    "_RequiredAnomalyGroupTimeSeriesTypeDef", {"AnomalyGroupId": str}
)
_OptionalAnomalyGroupTimeSeriesTypeDef = TypedDict(
    "_OptionalAnomalyGroupTimeSeriesTypeDef", {"TimeSeriesId": str}, total=False
)


class AnomalyGroupTimeSeriesTypeDef(
    _RequiredAnomalyGroupTimeSeriesTypeDef, _OptionalAnomalyGroupTimeSeriesTypeDef
):
    pass


CreateAlertResponseTypeDef = TypedDict("CreateAlertResponseTypeDef", {"AlertArn": str}, total=False)

CreateAnomalyDetectorResponseTypeDef = TypedDict(
    "CreateAnomalyDetectorResponseTypeDef", {"AnomalyDetectorArn": str}, total=False
)

CreateMetricSetResponseTypeDef = TypedDict(
    "CreateMetricSetResponseTypeDef", {"MetricSetArn": str}, total=False
)

DescribeAlertResponseTypeDef = TypedDict(
    "DescribeAlertResponseTypeDef", {"Alert": "AlertTypeDef"}, total=False
)

DescribeAnomalyDetectionExecutionsResponseTypeDef = TypedDict(
    "DescribeAnomalyDetectionExecutionsResponseTypeDef",
    {"ExecutionList": List["ExecutionStatusTypeDef"], "NextToken": str},
    total=False,
)

DescribeAnomalyDetectorResponseTypeDef = TypedDict(
    "DescribeAnomalyDetectorResponseTypeDef",
    {
        "AnomalyDetectorArn": str,
        "AnomalyDetectorName": str,
        "AnomalyDetectorDescription": str,
        "AnomalyDetectorConfig": "AnomalyDetectorConfigSummaryTypeDef",
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Status": Literal[
            "ACTIVE",
            "ACTIVATING",
            "DELETING",
            "FAILED",
            "INACTIVE",
            "BACK_TEST_ACTIVATING",
            "BACK_TEST_ACTIVE",
            "BACK_TEST_COMPLETE",
        ],
        "FailureReason": str,
        "KmsKeyArn": str,
    },
    total=False,
)

DescribeMetricSetResponseTypeDef = TypedDict(
    "DescribeMetricSetResponseTypeDef",
    {
        "MetricSetArn": str,
        "AnomalyDetectorArn": str,
        "MetricSetName": str,
        "MetricSetDescription": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Offset": int,
        "MetricList": List["MetricTypeDef"],
        "TimestampColumn": "TimestampColumnTypeDef",
        "DimensionList": List[str],
        "MetricSetFrequency": Literal["P1D", "PT1H", "PT10M", "PT5M"],
        "Timezone": str,
        "MetricSource": "MetricSourceTypeDef",
    },
    total=False,
)

GetAnomalyGroupResponseTypeDef = TypedDict(
    "GetAnomalyGroupResponseTypeDef", {"AnomalyGroup": "AnomalyGroupTypeDef"}, total=False
)

GetFeedbackResponseTypeDef = TypedDict(
    "GetFeedbackResponseTypeDef",
    {"AnomalyGroupTimeSeriesFeedback": List["TimeSeriesFeedbackTypeDef"], "NextToken": str},
    total=False,
)

GetSampleDataResponseTypeDef = TypedDict(
    "GetSampleDataResponseTypeDef",
    {"HeaderValues": List[str], "SampleRows": List[List[str]]},
    total=False,
)

ListAlertsResponseTypeDef = TypedDict(
    "ListAlertsResponseTypeDef",
    {"AlertSummaryList": List["AlertSummaryTypeDef"], "NextToken": str},
    total=False,
)

ListAnomalyDetectorsResponseTypeDef = TypedDict(
    "ListAnomalyDetectorsResponseTypeDef",
    {"AnomalyDetectorSummaryList": List["AnomalyDetectorSummaryTypeDef"], "NextToken": str},
    total=False,
)

ListAnomalyGroupSummariesResponseTypeDef = TypedDict(
    "ListAnomalyGroupSummariesResponseTypeDef",
    {
        "AnomalyGroupSummaryList": List["AnomalyGroupSummaryTypeDef"],
        "AnomalyGroupStatistics": "AnomalyGroupStatisticsTypeDef",
        "NextToken": str,
    },
    total=False,
)

ListAnomalyGroupTimeSeriesResponseTypeDef = TypedDict(
    "ListAnomalyGroupTimeSeriesResponseTypeDef",
    {
        "AnomalyGroupId": str,
        "MetricName": str,
        "TimestampList": List[str],
        "NextToken": str,
        "TimeSeriesList": List["TimeSeriesTypeDef"],
    },
    total=False,
)

ListMetricSetsResponseTypeDef = TypedDict(
    "ListMetricSetsResponseTypeDef",
    {"MetricSetSummaryList": List["MetricSetSummaryTypeDef"], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

_RequiredSampleDataS3SourceConfigTypeDef = TypedDict(
    "_RequiredSampleDataS3SourceConfigTypeDef",
    {"RoleArn": str, "FileFormatDescriptor": "FileFormatDescriptorTypeDef"},
)
_OptionalSampleDataS3SourceConfigTypeDef = TypedDict(
    "_OptionalSampleDataS3SourceConfigTypeDef",
    {"TemplatedPathList": List[str], "HistoricalDataPathList": List[str]},
    total=False,
)


class SampleDataS3SourceConfigTypeDef(
    _RequiredSampleDataS3SourceConfigTypeDef, _OptionalSampleDataS3SourceConfigTypeDef
):
    pass


UpdateAnomalyDetectorResponseTypeDef = TypedDict(
    "UpdateAnomalyDetectorResponseTypeDef", {"AnomalyDetectorArn": str}, total=False
)

UpdateMetricSetResponseTypeDef = TypedDict(
    "UpdateMetricSetResponseTypeDef", {"MetricSetArn": str}, total=False
)
