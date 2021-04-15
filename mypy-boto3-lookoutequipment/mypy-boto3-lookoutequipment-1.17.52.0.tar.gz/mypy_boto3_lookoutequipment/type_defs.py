"""
Main interface for lookoutequipment service type definitions.

Usage::

    ```python
    from mypy_boto3_lookoutequipment.type_defs import DataIngestionJobSummaryTypeDef

    data: DataIngestionJobSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DataIngestionJobSummaryTypeDef",
    "DataPreProcessingConfigurationTypeDef",
    "DatasetSummaryTypeDef",
    "InferenceExecutionSummaryTypeDef",
    "InferenceInputConfigurationTypeDef",
    "InferenceInputNameConfigurationTypeDef",
    "InferenceOutputConfigurationTypeDef",
    "InferenceS3InputConfigurationTypeDef",
    "InferenceS3OutputConfigurationTypeDef",
    "InferenceSchedulerSummaryTypeDef",
    "IngestionInputConfigurationTypeDef",
    "IngestionS3InputConfigurationTypeDef",
    "LabelsInputConfigurationTypeDef",
    "LabelsS3InputConfigurationTypeDef",
    "ModelSummaryTypeDef",
    "S3ObjectTypeDef",
    "TagTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateInferenceSchedulerResponseTypeDef",
    "CreateModelResponseTypeDef",
    "DatasetSchemaTypeDef",
    "DescribeDataIngestionJobResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeInferenceSchedulerResponseTypeDef",
    "DescribeModelResponseTypeDef",
    "ListDataIngestionJobsResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListInferenceExecutionsResponseTypeDef",
    "ListInferenceSchedulersResponseTypeDef",
    "ListModelsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartDataIngestionJobResponseTypeDef",
    "StartInferenceSchedulerResponseTypeDef",
    "StopInferenceSchedulerResponseTypeDef",
)

DataIngestionJobSummaryTypeDef = TypedDict(
    "DataIngestionJobSummaryTypeDef",
    {
        "JobId": str,
        "DatasetName": str,
        "DatasetArn": str,
        "IngestionInputConfiguration": "IngestionInputConfigurationTypeDef",
        "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"],
    },
    total=False,
)

DataPreProcessingConfigurationTypeDef = TypedDict(
    "DataPreProcessingConfigurationTypeDef",
    {
        "TargetSamplingRate": Literal[
            "PT1S",
            "PT5S",
            "PT10S",
            "PT15S",
            "PT30S",
            "PT1M",
            "PT5M",
            "PT10M",
            "PT15M",
            "PT30M",
            "PT1H",
        ]
    },
    total=False,
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "Status": Literal["CREATED", "INGESTION_IN_PROGRESS", "ACTIVE"],
        "CreatedAt": datetime,
    },
    total=False,
)

InferenceExecutionSummaryTypeDef = TypedDict(
    "InferenceExecutionSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "ScheduledStartTime": datetime,
        "DataStartTime": datetime,
        "DataEndTime": datetime,
        "DataInputConfiguration": "InferenceInputConfigurationTypeDef",
        "DataOutputConfiguration": "InferenceOutputConfigurationTypeDef",
        "CustomerResultObject": "S3ObjectTypeDef",
        "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"],
        "FailedReason": str,
    },
    total=False,
)

InferenceInputConfigurationTypeDef = TypedDict(
    "InferenceInputConfigurationTypeDef",
    {
        "S3InputConfiguration": "InferenceS3InputConfigurationTypeDef",
        "InputTimeZoneOffset": str,
        "InferenceInputNameConfiguration": "InferenceInputNameConfigurationTypeDef",
    },
    total=False,
)

InferenceInputNameConfigurationTypeDef = TypedDict(
    "InferenceInputNameConfigurationTypeDef",
    {"TimestampFormat": str, "ComponentTimestampDelimiter": str},
    total=False,
)

_RequiredInferenceOutputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceOutputConfigurationTypeDef",
    {"S3OutputConfiguration": "InferenceS3OutputConfigurationTypeDef"},
)
_OptionalInferenceOutputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceOutputConfigurationTypeDef", {"KmsKeyId": str}, total=False
)


class InferenceOutputConfigurationTypeDef(
    _RequiredInferenceOutputConfigurationTypeDef, _OptionalInferenceOutputConfigurationTypeDef
):
    pass


_RequiredInferenceS3InputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceS3InputConfigurationTypeDef", {"Bucket": str}
)
_OptionalInferenceS3InputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceS3InputConfigurationTypeDef", {"Prefix": str}, total=False
)


class InferenceS3InputConfigurationTypeDef(
    _RequiredInferenceS3InputConfigurationTypeDef, _OptionalInferenceS3InputConfigurationTypeDef
):
    pass


_RequiredInferenceS3OutputConfigurationTypeDef = TypedDict(
    "_RequiredInferenceS3OutputConfigurationTypeDef", {"Bucket": str}
)
_OptionalInferenceS3OutputConfigurationTypeDef = TypedDict(
    "_OptionalInferenceS3OutputConfigurationTypeDef", {"Prefix": str}, total=False
)


class InferenceS3OutputConfigurationTypeDef(
    _RequiredInferenceS3OutputConfigurationTypeDef, _OptionalInferenceS3OutputConfigurationTypeDef
):
    pass


InferenceSchedulerSummaryTypeDef = TypedDict(
    "InferenceSchedulerSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": Literal["PENDING", "RUNNING", "STOPPING", "STOPPED"],
        "DataDelayOffsetInMinutes": int,
        "DataUploadFrequency": Literal["PT5M", "PT10M", "PT15M", "PT30M", "PT1H"],
    },
    total=False,
)

IngestionInputConfigurationTypeDef = TypedDict(
    "IngestionInputConfigurationTypeDef",
    {"S3InputConfiguration": "IngestionS3InputConfigurationTypeDef"},
)

_RequiredIngestionS3InputConfigurationTypeDef = TypedDict(
    "_RequiredIngestionS3InputConfigurationTypeDef", {"Bucket": str}
)
_OptionalIngestionS3InputConfigurationTypeDef = TypedDict(
    "_OptionalIngestionS3InputConfigurationTypeDef", {"Prefix": str}, total=False
)


class IngestionS3InputConfigurationTypeDef(
    _RequiredIngestionS3InputConfigurationTypeDef, _OptionalIngestionS3InputConfigurationTypeDef
):
    pass


LabelsInputConfigurationTypeDef = TypedDict(
    "LabelsInputConfigurationTypeDef", {"S3InputConfiguration": "LabelsS3InputConfigurationTypeDef"}
)

_RequiredLabelsS3InputConfigurationTypeDef = TypedDict(
    "_RequiredLabelsS3InputConfigurationTypeDef", {"Bucket": str}
)
_OptionalLabelsS3InputConfigurationTypeDef = TypedDict(
    "_OptionalLabelsS3InputConfigurationTypeDef", {"Prefix": str}, total=False
)


class LabelsS3InputConfigurationTypeDef(
    _RequiredLabelsS3InputConfigurationTypeDef, _OptionalLabelsS3InputConfigurationTypeDef
):
    pass


ModelSummaryTypeDef = TypedDict(
    "ModelSummaryTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "DatasetName": str,
        "DatasetArn": str,
        "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"],
        "CreatedAt": datetime,
    },
    total=False,
)

S3ObjectTypeDef = TypedDict("S3ObjectTypeDef", {"Bucket": str, "Key": str})

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "Status": Literal["CREATED", "INGESTION_IN_PROGRESS", "ACTIVE"],
    },
    total=False,
)

CreateInferenceSchedulerResponseTypeDef = TypedDict(
    "CreateInferenceSchedulerResponseTypeDef",
    {
        "InferenceSchedulerArn": str,
        "InferenceSchedulerName": str,
        "Status": Literal["PENDING", "RUNNING", "STOPPING", "STOPPED"],
    },
    total=False,
)

CreateModelResponseTypeDef = TypedDict(
    "CreateModelResponseTypeDef",
    {"ModelArn": str, "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"]},
    total=False,
)

DatasetSchemaTypeDef = TypedDict("DatasetSchemaTypeDef", {"InlineDataSchema": str}, total=False)

DescribeDataIngestionJobResponseTypeDef = TypedDict(
    "DescribeDataIngestionJobResponseTypeDef",
    {
        "JobId": str,
        "DatasetArn": str,
        "IngestionInputConfiguration": "IngestionInputConfigurationTypeDef",
        "RoleArn": str,
        "CreatedAt": datetime,
        "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"],
        "FailedReason": str,
    },
    total=False,
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetName": str,
        "DatasetArn": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Status": Literal["CREATED", "INGESTION_IN_PROGRESS", "ACTIVE"],
        "Schema": str,
        "ServerSideKmsKeyId": str,
        "IngestionInputConfiguration": "IngestionInputConfigurationTypeDef",
    },
    total=False,
)

DescribeInferenceSchedulerResponseTypeDef = TypedDict(
    "DescribeInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": Literal["PENDING", "RUNNING", "STOPPING", "STOPPED"],
        "DataDelayOffsetInMinutes": int,
        "DataUploadFrequency": Literal["PT5M", "PT10M", "PT15M", "PT30M", "PT1H"],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "DataInputConfiguration": "InferenceInputConfigurationTypeDef",
        "DataOutputConfiguration": "InferenceOutputConfigurationTypeDef",
        "RoleArn": str,
        "ServerSideKmsKeyId": str,
    },
    total=False,
)

DescribeModelResponseTypeDef = TypedDict(
    "DescribeModelResponseTypeDef",
    {
        "ModelName": str,
        "ModelArn": str,
        "DatasetName": str,
        "DatasetArn": str,
        "Schema": str,
        "LabelsInputConfiguration": "LabelsInputConfigurationTypeDef",
        "TrainingDataStartTime": datetime,
        "TrainingDataEndTime": datetime,
        "EvaluationDataStartTime": datetime,
        "EvaluationDataEndTime": datetime,
        "RoleArn": str,
        "DataPreProcessingConfiguration": "DataPreProcessingConfigurationTypeDef",
        "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"],
        "TrainingExecutionStartTime": datetime,
        "TrainingExecutionEndTime": datetime,
        "FailedReason": str,
        "ModelMetrics": str,
        "LastUpdatedTime": datetime,
        "CreatedAt": datetime,
        "ServerSideKmsKeyId": str,
    },
    total=False,
)

ListDataIngestionJobsResponseTypeDef = TypedDict(
    "ListDataIngestionJobsResponseTypeDef",
    {"NextToken": str, "DataIngestionJobSummaries": List["DataIngestionJobSummaryTypeDef"]},
    total=False,
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {"NextToken": str, "DatasetSummaries": List["DatasetSummaryTypeDef"]},
    total=False,
)

ListInferenceExecutionsResponseTypeDef = TypedDict(
    "ListInferenceExecutionsResponseTypeDef",
    {"NextToken": str, "InferenceExecutionSummaries": List["InferenceExecutionSummaryTypeDef"]},
    total=False,
)

ListInferenceSchedulersResponseTypeDef = TypedDict(
    "ListInferenceSchedulersResponseTypeDef",
    {"NextToken": str, "InferenceSchedulerSummaries": List["InferenceSchedulerSummaryTypeDef"]},
    total=False,
)

ListModelsResponseTypeDef = TypedDict(
    "ListModelsResponseTypeDef",
    {"NextToken": str, "ModelSummaries": List["ModelSummaryTypeDef"]},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

StartDataIngestionJobResponseTypeDef = TypedDict(
    "StartDataIngestionJobResponseTypeDef",
    {"JobId": str, "Status": Literal["IN_PROGRESS", "SUCCESS", "FAILED"]},
    total=False,
)

StartInferenceSchedulerResponseTypeDef = TypedDict(
    "StartInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": Literal["PENDING", "RUNNING", "STOPPING", "STOPPED"],
    },
    total=False,
)

StopInferenceSchedulerResponseTypeDef = TypedDict(
    "StopInferenceSchedulerResponseTypeDef",
    {
        "ModelArn": str,
        "ModelName": str,
        "InferenceSchedulerName": str,
        "InferenceSchedulerArn": str,
        "Status": Literal["PENDING", "RUNNING", "STOPPING", "STOPPED"],
    },
    total=False,
)
