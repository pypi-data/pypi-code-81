"""
Main interface for lookoutmetrics service client

Usage::

    ```python
    import boto3
    from mypy_boto3_lookoutmetrics import LookoutMetricsClient

    client: LookoutMetricsClient = boto3.client("lookoutmetrics")
    ```
"""
import sys
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from mypy_boto3_lookoutmetrics.type_defs import (
    ActionTypeDef,
    AnomalyDetectorConfigTypeDef,
    AnomalyGroupTimeSeriesFeedbackTypeDef,
    AnomalyGroupTimeSeriesTypeDef,
    CreateAlertResponseTypeDef,
    CreateAnomalyDetectorResponseTypeDef,
    CreateMetricSetResponseTypeDef,
    DescribeAlertResponseTypeDef,
    DescribeAnomalyDetectionExecutionsResponseTypeDef,
    DescribeAnomalyDetectorResponseTypeDef,
    DescribeMetricSetResponseTypeDef,
    GetAnomalyGroupResponseTypeDef,
    GetFeedbackResponseTypeDef,
    GetSampleDataResponseTypeDef,
    ListAlertsResponseTypeDef,
    ListAnomalyDetectorsResponseTypeDef,
    ListAnomalyGroupSummariesResponseTypeDef,
    ListAnomalyGroupTimeSeriesResponseTypeDef,
    ListMetricSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MetricSourceTypeDef,
    MetricTypeDef,
    SampleDataS3SourceConfigTypeDef,
    TimestampColumnTypeDef,
    UpdateAnomalyDetectorResponseTypeDef,
    UpdateMetricSetResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LookoutMetricsClient",)


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
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LookoutMetricsClient:
    """
    [LookoutMetrics.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def activate_anomaly_detector(self, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        [Client.activate_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.activate_anomaly_detector)
        """

    def back_test_anomaly_detector(self, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        [Client.back_test_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.back_test_anomaly_detector)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.can_paginate)
        """

    def create_alert(
        self,
        AlertName: str,
        AlertSensitivityThreshold: int,
        AnomalyDetectorArn: str,
        Action: "ActionTypeDef",
        AlertDescription: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateAlertResponseTypeDef:
        """
        [Client.create_alert documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_alert)
        """

    def create_anomaly_detector(
        self,
        AnomalyDetectorName: str,
        AnomalyDetectorConfig: AnomalyDetectorConfigTypeDef,
        AnomalyDetectorDescription: str = None,
        KmsKeyArn: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateAnomalyDetectorResponseTypeDef:
        """
        [Client.create_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_anomaly_detector)
        """

    def create_metric_set(
        self,
        AnomalyDetectorArn: str,
        MetricSetName: str,
        MetricList: List["MetricTypeDef"],
        MetricSource: "MetricSourceTypeDef",
        MetricSetDescription: str = None,
        Offset: int = None,
        TimestampColumn: "TimestampColumnTypeDef" = None,
        DimensionList: List[str] = None,
        MetricSetFrequency: Literal["P1D", "PT1H", "PT10M", "PT5M"] = None,
        Timezone: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateMetricSetResponseTypeDef:
        """
        [Client.create_metric_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_metric_set)
        """

    def delete_alert(self, AlertArn: str) -> Dict[str, Any]:
        """
        [Client.delete_alert documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.delete_alert)
        """

    def delete_anomaly_detector(self, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        [Client.delete_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.delete_anomaly_detector)
        """

    def describe_alert(self, AlertArn: str) -> DescribeAlertResponseTypeDef:
        """
        [Client.describe_alert documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_alert)
        """

    def describe_anomaly_detection_executions(
        self,
        AnomalyDetectorArn: str,
        Timestamp: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> DescribeAnomalyDetectionExecutionsResponseTypeDef:
        """
        [Client.describe_anomaly_detection_executions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_anomaly_detection_executions)
        """

    def describe_anomaly_detector(
        self, AnomalyDetectorArn: str
    ) -> DescribeAnomalyDetectorResponseTypeDef:
        """
        [Client.describe_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_anomaly_detector)
        """

    def describe_metric_set(self, MetricSetArn: str) -> DescribeMetricSetResponseTypeDef:
        """
        [Client.describe_metric_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_metric_set)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.generate_presigned_url)
        """

    def get_anomaly_group(
        self, AnomalyGroupId: str, AnomalyDetectorArn: str
    ) -> GetAnomalyGroupResponseTypeDef:
        """
        [Client.get_anomaly_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_anomaly_group)
        """

    def get_feedback(
        self,
        AnomalyDetectorArn: str,
        AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesTypeDef,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> GetFeedbackResponseTypeDef:
        """
        [Client.get_feedback documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_feedback)
        """

    def get_sample_data(
        self, S3SourceConfig: SampleDataS3SourceConfigTypeDef = None
    ) -> GetSampleDataResponseTypeDef:
        """
        [Client.get_sample_data documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_sample_data)
        """

    def list_alerts(
        self, AnomalyDetectorArn: str = None, NextToken: str = None, MaxResults: int = None
    ) -> ListAlertsResponseTypeDef:
        """
        [Client.list_alerts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_alerts)
        """

    def list_anomaly_detectors(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListAnomalyDetectorsResponseTypeDef:
        """
        [Client.list_anomaly_detectors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_detectors)
        """

    def list_anomaly_group_summaries(
        self,
        AnomalyDetectorArn: str,
        SensitivityThreshold: int,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListAnomalyGroupSummariesResponseTypeDef:
        """
        [Client.list_anomaly_group_summaries documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_group_summaries)
        """

    def list_anomaly_group_time_series(
        self,
        AnomalyDetectorArn: str,
        AnomalyGroupId: str,
        MetricName: str,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListAnomalyGroupTimeSeriesResponseTypeDef:
        """
        [Client.list_anomaly_group_time_series documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_group_time_series)
        """

    def list_metric_sets(
        self, AnomalyDetectorArn: str = None, MaxResults: int = None, NextToken: str = None
    ) -> ListMetricSetsResponseTypeDef:
        """
        [Client.list_metric_sets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_metric_sets)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_tags_for_resource)
        """

    def put_feedback(
        self,
        AnomalyDetectorArn: str,
        AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesFeedbackTypeDef,
    ) -> Dict[str, Any]:
        """
        [Client.put_feedback documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.put_feedback)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.untag_resource)
        """

    def update_anomaly_detector(
        self,
        AnomalyDetectorArn: str,
        KmsKeyArn: str = None,
        AnomalyDetectorDescription: str = None,
        AnomalyDetectorConfig: AnomalyDetectorConfigTypeDef = None,
    ) -> UpdateAnomalyDetectorResponseTypeDef:
        """
        [Client.update_anomaly_detector documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.update_anomaly_detector)
        """

    def update_metric_set(
        self,
        MetricSetArn: str,
        MetricSetDescription: str = None,
        MetricList: List["MetricTypeDef"] = None,
        Offset: int = None,
        TimestampColumn: "TimestampColumnTypeDef" = None,
        DimensionList: List[str] = None,
        MetricSetFrequency: Literal["P1D", "PT1H", "PT10M", "PT5M"] = None,
        MetricSource: "MetricSourceTypeDef" = None,
    ) -> UpdateMetricSetResponseTypeDef:
        """
        [Client.update_metric_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutmetrics.html#LookoutMetrics.Client.update_metric_set)
        """
