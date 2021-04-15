"""
Main interface for fis service type definitions.

Usage::

    ```python
    from mypy_boto3_fis.type_defs import ActionParameterTypeDef

    data: ActionParameterTypeDef = {...}
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
    "ActionParameterTypeDef",
    "ActionSummaryTypeDef",
    "ActionTargetTypeDef",
    "ActionTypeDef",
    "ExperimentActionStateTypeDef",
    "ExperimentActionTypeDef",
    "ExperimentStateTypeDef",
    "ExperimentStopConditionTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTargetFilterTypeDef",
    "ExperimentTargetTypeDef",
    "ExperimentTemplateActionTypeDef",
    "ExperimentTemplateStopConditionTypeDef",
    "ExperimentTemplateSummaryTypeDef",
    "ExperimentTemplateTargetFilterTypeDef",
    "ExperimentTemplateTargetInputFilterTypeDef",
    "ExperimentTemplateTargetTypeDef",
    "ExperimentTemplateTypeDef",
    "ExperimentTypeDef",
    "CreateExperimentTemplateActionInputTypeDef",
    "CreateExperimentTemplateResponseTypeDef",
    "CreateExperimentTemplateStopConditionInputTypeDef",
    "CreateExperimentTemplateTargetInputTypeDef",
    "DeleteExperimentTemplateResponseTypeDef",
    "GetActionResponseTypeDef",
    "GetExperimentResponseTypeDef",
    "GetExperimentTemplateResponseTypeDef",
    "ListActionsResponseTypeDef",
    "ListExperimentTemplatesResponseTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartExperimentResponseTypeDef",
    "StopExperimentResponseTypeDef",
    "UpdateExperimentTemplateActionInputItemTypeDef",
    "UpdateExperimentTemplateResponseTypeDef",
    "UpdateExperimentTemplateStopConditionInputTypeDef",
    "UpdateExperimentTemplateTargetInputTypeDef",
)

ActionParameterTypeDef = TypedDict(
    "ActionParameterTypeDef", {"description": str, "required": bool}, total=False
)

ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "id": str,
        "description": str,
        "targets": Dict[str, "ActionTargetTypeDef"],
        "tags": Dict[str, str],
    },
    total=False,
)

ActionTargetTypeDef = TypedDict("ActionTargetTypeDef", {"resourceType": str}, total=False)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "id": str,
        "description": str,
        "parameters": Dict[str, "ActionParameterTypeDef"],
        "targets": Dict[str, "ActionTargetTypeDef"],
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentActionStateTypeDef = TypedDict(
    "ExperimentActionStateTypeDef",
    {
        "status": Literal[
            "pending",
            "initiating",
            "running",
            "completed",
            "cancelled",
            "stopping",
            "stopped",
            "failed",
        ],
        "reason": str,
    },
    total=False,
)

ExperimentActionTypeDef = TypedDict(
    "ExperimentActionTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
        "state": "ExperimentActionStateTypeDef",
    },
    total=False,
)

ExperimentStateTypeDef = TypedDict(
    "ExperimentStateTypeDef",
    {
        "status": Literal[
            "pending", "initiating", "running", "completed", "stopping", "stopped", "failed"
        ],
        "reason": str,
    },
    total=False,
)

ExperimentStopConditionTypeDef = TypedDict(
    "ExperimentStopConditionTypeDef", {"source": str, "value": str}, total=False
)

ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "id": str,
        "experimentTemplateId": str,
        "state": "ExperimentStateTypeDef",
        "creationTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentTargetFilterTypeDef = TypedDict(
    "ExperimentTargetFilterTypeDef", {"path": str, "values": List[str]}, total=False
)

ExperimentTargetTypeDef = TypedDict(
    "ExperimentTargetTypeDef",
    {
        "resourceType": str,
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List["ExperimentTargetFilterTypeDef"],
        "selectionMode": str,
    },
    total=False,
)

ExperimentTemplateActionTypeDef = TypedDict(
    "ExperimentTemplateActionTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
    },
    total=False,
)

ExperimentTemplateStopConditionTypeDef = TypedDict(
    "ExperimentTemplateStopConditionTypeDef", {"source": str, "value": str}, total=False
)

ExperimentTemplateSummaryTypeDef = TypedDict(
    "ExperimentTemplateSummaryTypeDef",
    {
        "id": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentTemplateTargetFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetFilterTypeDef", {"path": str, "values": List[str]}, total=False
)

ExperimentTemplateTargetInputFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetInputFilterTypeDef", {"path": str, "values": List[str]}
)

ExperimentTemplateTargetTypeDef = TypedDict(
    "ExperimentTemplateTargetTypeDef",
    {
        "resourceType": str,
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List["ExperimentTemplateTargetFilterTypeDef"],
        "selectionMode": str,
    },
    total=False,
)

ExperimentTemplateTypeDef = TypedDict(
    "ExperimentTemplateTypeDef",
    {
        "id": str,
        "description": str,
        "targets": Dict[str, "ExperimentTemplateTargetTypeDef"],
        "actions": Dict[str, "ExperimentTemplateActionTypeDef"],
        "stopConditions": List["ExperimentTemplateStopConditionTypeDef"],
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "roleArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "id": str,
        "experimentTemplateId": str,
        "roleArn": str,
        "state": "ExperimentStateTypeDef",
        "targets": Dict[str, "ExperimentTargetTypeDef"],
        "actions": Dict[str, "ExperimentActionTypeDef"],
        "stopConditions": List["ExperimentStopConditionTypeDef"],
        "creationTime": datetime,
        "startTime": datetime,
        "endTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredCreateExperimentTemplateActionInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateActionInputTypeDef", {"actionId": str}
)
_OptionalCreateExperimentTemplateActionInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateActionInputTypeDef",
    {
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
    },
    total=False,
)


class CreateExperimentTemplateActionInputTypeDef(
    _RequiredCreateExperimentTemplateActionInputTypeDef,
    _OptionalCreateExperimentTemplateActionInputTypeDef,
):
    pass


CreateExperimentTemplateResponseTypeDef = TypedDict(
    "CreateExperimentTemplateResponseTypeDef",
    {"experimentTemplate": "ExperimentTemplateTypeDef"},
    total=False,
)

_RequiredCreateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateStopConditionInputTypeDef", {"source": str}
)
_OptionalCreateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateStopConditionInputTypeDef", {"value": str}, total=False
)


class CreateExperimentTemplateStopConditionInputTypeDef(
    _RequiredCreateExperimentTemplateStopConditionInputTypeDef,
    _OptionalCreateExperimentTemplateStopConditionInputTypeDef,
):
    pass


_RequiredCreateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateTargetInputTypeDef",
    {"resourceType": str, "selectionMode": str},
)
_OptionalCreateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateTargetInputTypeDef",
    {
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List["ExperimentTemplateTargetInputFilterTypeDef"],
    },
    total=False,
)


class CreateExperimentTemplateTargetInputTypeDef(
    _RequiredCreateExperimentTemplateTargetInputTypeDef,
    _OptionalCreateExperimentTemplateTargetInputTypeDef,
):
    pass


DeleteExperimentTemplateResponseTypeDef = TypedDict(
    "DeleteExperimentTemplateResponseTypeDef",
    {"experimentTemplate": "ExperimentTemplateTypeDef"},
    total=False,
)

GetActionResponseTypeDef = TypedDict(
    "GetActionResponseTypeDef", {"action": "ActionTypeDef"}, total=False
)

GetExperimentResponseTypeDef = TypedDict(
    "GetExperimentResponseTypeDef", {"experiment": "ExperimentTypeDef"}, total=False
)

GetExperimentTemplateResponseTypeDef = TypedDict(
    "GetExperimentTemplateResponseTypeDef",
    {"experimentTemplate": "ExperimentTemplateTypeDef"},
    total=False,
)

ListActionsResponseTypeDef = TypedDict(
    "ListActionsResponseTypeDef",
    {"actions": List["ActionSummaryTypeDef"], "nextToken": str},
    total=False,
)

ListExperimentTemplatesResponseTypeDef = TypedDict(
    "ListExperimentTemplatesResponseTypeDef",
    {"experimentTemplates": List["ExperimentTemplateSummaryTypeDef"], "nextToken": str},
    total=False,
)

ListExperimentsResponseTypeDef = TypedDict(
    "ListExperimentsResponseTypeDef",
    {"experiments": List["ExperimentSummaryTypeDef"], "nextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

StartExperimentResponseTypeDef = TypedDict(
    "StartExperimentResponseTypeDef", {"experiment": "ExperimentTypeDef"}, total=False
)

StopExperimentResponseTypeDef = TypedDict(
    "StopExperimentResponseTypeDef", {"experiment": "ExperimentTypeDef"}, total=False
)

UpdateExperimentTemplateActionInputItemTypeDef = TypedDict(
    "UpdateExperimentTemplateActionInputItemTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
    },
    total=False,
)

UpdateExperimentTemplateResponseTypeDef = TypedDict(
    "UpdateExperimentTemplateResponseTypeDef",
    {"experimentTemplate": "ExperimentTemplateTypeDef"},
    total=False,
)

_RequiredUpdateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_RequiredUpdateExperimentTemplateStopConditionInputTypeDef", {"source": str}
)
_OptionalUpdateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_OptionalUpdateExperimentTemplateStopConditionInputTypeDef", {"value": str}, total=False
)


class UpdateExperimentTemplateStopConditionInputTypeDef(
    _RequiredUpdateExperimentTemplateStopConditionInputTypeDef,
    _OptionalUpdateExperimentTemplateStopConditionInputTypeDef,
):
    pass


_RequiredUpdateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_RequiredUpdateExperimentTemplateTargetInputTypeDef",
    {"resourceType": str, "selectionMode": str},
)
_OptionalUpdateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_OptionalUpdateExperimentTemplateTargetInputTypeDef",
    {
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List["ExperimentTemplateTargetInputFilterTypeDef"],
    },
    total=False,
)


class UpdateExperimentTemplateTargetInputTypeDef(
    _RequiredUpdateExperimentTemplateTargetInputTypeDef,
    _OptionalUpdateExperimentTemplateTargetInputTypeDef,
):
    pass
