"""
Main interface for lookoutequipment service client

Usage::

    ```python
    import boto3
    from mypy_boto3_lookoutequipment import LookoutEquipmentClient

    client: LookoutEquipmentClient = boto3.client("lookoutequipment")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from mypy_boto3_lookoutequipment.type_defs import (
    CreateDatasetResponseTypeDef,
    CreateInferenceSchedulerResponseTypeDef,
    CreateModelResponseTypeDef,
    DataPreProcessingConfigurationTypeDef,
    DatasetSchemaTypeDef,
    DescribeDataIngestionJobResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeInferenceSchedulerResponseTypeDef,
    DescribeModelResponseTypeDef,
    InferenceInputConfigurationTypeDef,
    InferenceOutputConfigurationTypeDef,
    IngestionInputConfigurationTypeDef,
    LabelsInputConfigurationTypeDef,
    ListDataIngestionJobsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListInferenceExecutionsResponseTypeDef,
    ListInferenceSchedulersResponseTypeDef,
    ListModelsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartDataIngestionJobResponseTypeDef,
    StartInferenceSchedulerResponseTypeDef,
    StopInferenceSchedulerResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LookoutEquipmentClient",)


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


class LookoutEquipmentClient:
    """
    [LookoutEquipment.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.can_paginate)
        """

    def create_dataset(
        self,
        DatasetName: str,
        DatasetSchema: DatasetSchemaTypeDef,
        ClientToken: str,
        ServerSideKmsKeyId: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateDatasetResponseTypeDef:
        """
        [Client.create_dataset documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_dataset)
        """

    def create_inference_scheduler(
        self,
        ModelName: str,
        InferenceSchedulerName: str,
        DataUploadFrequency: Literal["PT5M", "PT10M", "PT15M", "PT30M", "PT1H"],
        DataInputConfiguration: "InferenceInputConfigurationTypeDef",
        DataOutputConfiguration: "InferenceOutputConfigurationTypeDef",
        RoleArn: str,
        ClientToken: str,
        DataDelayOffsetInMinutes: int = None,
        ServerSideKmsKeyId: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateInferenceSchedulerResponseTypeDef:
        """
        [Client.create_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_inference_scheduler)
        """

    def create_model(
        self,
        ModelName: str,
        DatasetName: str,
        ClientToken: str,
        DatasetSchema: DatasetSchemaTypeDef = None,
        LabelsInputConfiguration: "LabelsInputConfigurationTypeDef" = None,
        TrainingDataStartTime: datetime = None,
        TrainingDataEndTime: datetime = None,
        EvaluationDataStartTime: datetime = None,
        EvaluationDataEndTime: datetime = None,
        RoleArn: str = None,
        DataPreProcessingConfiguration: "DataPreProcessingConfigurationTypeDef" = None,
        ServerSideKmsKeyId: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateModelResponseTypeDef:
        """
        [Client.create_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_model)
        """

    def delete_dataset(self, DatasetName: str) -> None:
        """
        [Client.delete_dataset documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_dataset)
        """

    def delete_inference_scheduler(self, InferenceSchedulerName: str) -> None:
        """
        [Client.delete_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_inference_scheduler)
        """

    def delete_model(self, ModelName: str) -> None:
        """
        [Client.delete_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_model)
        """

    def describe_data_ingestion_job(self, JobId: str) -> DescribeDataIngestionJobResponseTypeDef:
        """
        [Client.describe_data_ingestion_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_data_ingestion_job)
        """

    def describe_dataset(self, DatasetName: str) -> DescribeDatasetResponseTypeDef:
        """
        [Client.describe_dataset documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_dataset)
        """

    def describe_inference_scheduler(
        self, InferenceSchedulerName: str
    ) -> DescribeInferenceSchedulerResponseTypeDef:
        """
        [Client.describe_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_inference_scheduler)
        """

    def describe_model(self, ModelName: str) -> DescribeModelResponseTypeDef:
        """
        [Client.describe_model documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_model)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.generate_presigned_url)
        """

    def list_data_ingestion_jobs(
        self,
        DatasetName: str = None,
        NextToken: str = None,
        MaxResults: int = None,
        Status: Literal["IN_PROGRESS", "SUCCESS", "FAILED"] = None,
    ) -> ListDataIngestionJobsResponseTypeDef:
        """
        [Client.list_data_ingestion_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_data_ingestion_jobs)
        """

    def list_datasets(
        self, NextToken: str = None, MaxResults: int = None, DatasetNameBeginsWith: str = None
    ) -> ListDatasetsResponseTypeDef:
        """
        [Client.list_datasets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_datasets)
        """

    def list_inference_executions(
        self,
        InferenceSchedulerName: str,
        NextToken: str = None,
        MaxResults: int = None,
        DataStartTimeAfter: datetime = None,
        DataEndTimeBefore: datetime = None,
        Status: Literal["IN_PROGRESS", "SUCCESS", "FAILED"] = None,
    ) -> ListInferenceExecutionsResponseTypeDef:
        """
        [Client.list_inference_executions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_inference_executions)
        """

    def list_inference_schedulers(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        InferenceSchedulerNameBeginsWith: str = None,
        ModelName: str = None,
    ) -> ListInferenceSchedulersResponseTypeDef:
        """
        [Client.list_inference_schedulers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_inference_schedulers)
        """

    def list_models(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Status: Literal["IN_PROGRESS", "SUCCESS", "FAILED"] = None,
        ModelNameBeginsWith: str = None,
        DatasetNameBeginsWith: str = None,
    ) -> ListModelsResponseTypeDef:
        """
        [Client.list_models documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_models)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_tags_for_resource)
        """

    def start_data_ingestion_job(
        self,
        DatasetName: str,
        IngestionInputConfiguration: "IngestionInputConfigurationTypeDef",
        RoleArn: str,
        ClientToken: str,
    ) -> StartDataIngestionJobResponseTypeDef:
        """
        [Client.start_data_ingestion_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.start_data_ingestion_job)
        """

    def start_inference_scheduler(
        self, InferenceSchedulerName: str
    ) -> StartInferenceSchedulerResponseTypeDef:
        """
        [Client.start_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.start_inference_scheduler)
        """

    def stop_inference_scheduler(
        self, InferenceSchedulerName: str
    ) -> StopInferenceSchedulerResponseTypeDef:
        """
        [Client.stop_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.stop_inference_scheduler)
        """

    def tag_resource(self, ResourceArn: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.untag_resource)
        """

    def update_inference_scheduler(
        self,
        InferenceSchedulerName: str,
        DataDelayOffsetInMinutes: int = None,
        DataUploadFrequency: Literal["PT5M", "PT10M", "PT15M", "PT30M", "PT1H"] = None,
        DataInputConfiguration: "InferenceInputConfigurationTypeDef" = None,
        DataOutputConfiguration: "InferenceOutputConfigurationTypeDef" = None,
        RoleArn: str = None,
    ) -> None:
        """
        [Client.update_inference_scheduler documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.50/reference/services/lookoutequipment.html#LookoutEquipment.Client.update_inference_scheduler)
        """
