from dataclasses import dataclass
from typing import Union, Optional

from arthurai.common.constants import ListableStrEnum
from arthurai.core.base import ArthurBaseJsonDataclass, NumberType


class AlertMetric(ListableStrEnum):
    TotalInferenceCount = "Total Inference Count"
    TotalInferenceCountByClass = "Total Inference Count By Class"
    AveragePrediction = "Average Prediction"
    RMSE = "RMSE"
    PSIDataDriftReferenceSet = "PSI Data Drift Reference Set"
    PSIBatchDataDriftReferenceSet = "PSI Batch Data Drift Reference Set"
    TruePositiveRate = "True Positive Rate"
    TrueNegativeRate = "True Negative Rate"
    FalsePositiveRate = "False Positive Rate"
    FalseNegativeRate = "False Negative Rate"


class AlertRuleBound(ListableStrEnum):
    Upper = "upper"
    Lower = "lower"


class AlertRuleSeverity(ListableStrEnum):
    Warning = "warning"
    Critical = "critical"


@dataclass
class AlertRule(ArthurBaseJsonDataclass):
    bound: AlertRuleBound
    threshold: NumberType
    metric: Union[AlertMetric, str]
    severity: AlertRuleSeverity
    query: Optional[dict] = None
    lookback_period: Optional[NumberType] = None
    subsequent_alert_wait_time: Optional[NumberType] = None
    check_batch_idle_time: Optional[NumberType] = None
    attribute_id: Optional[str] = None
    attribute_name: Optional[str] = None
    enabled: bool = True
    id: Optional[str] = None
