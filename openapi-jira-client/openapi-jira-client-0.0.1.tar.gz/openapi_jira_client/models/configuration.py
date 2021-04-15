from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.time_tracking_configuration import TimeTrackingConfiguration
from ..types import UNSET, Unset

T = TypeVar("T", bound="Configuration")


@attr.s(auto_attribs=True)
class Configuration:
    """ Details about the configuration of Jira. """

    voting_enabled: Union[Unset, bool] = UNSET
    watching_enabled: Union[Unset, bool] = UNSET
    unassigned_issues_allowed: Union[Unset, bool] = UNSET
    sub_tasks_enabled: Union[Unset, bool] = UNSET
    issue_linking_enabled: Union[Unset, bool] = UNSET
    time_tracking_enabled: Union[Unset, bool] = UNSET
    attachments_enabled: Union[Unset, bool] = UNSET
    time_tracking_configuration: Union[Unset, TimeTrackingConfiguration] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        voting_enabled = self.voting_enabled
        watching_enabled = self.watching_enabled
        unassigned_issues_allowed = self.unassigned_issues_allowed
        sub_tasks_enabled = self.sub_tasks_enabled
        issue_linking_enabled = self.issue_linking_enabled
        time_tracking_enabled = self.time_tracking_enabled
        attachments_enabled = self.attachments_enabled
        time_tracking_configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.time_tracking_configuration, Unset):
            time_tracking_configuration = self.time_tracking_configuration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if voting_enabled is not UNSET:
            field_dict["votingEnabled"] = voting_enabled
        if watching_enabled is not UNSET:
            field_dict["watchingEnabled"] = watching_enabled
        if unassigned_issues_allowed is not UNSET:
            field_dict["unassignedIssuesAllowed"] = unassigned_issues_allowed
        if sub_tasks_enabled is not UNSET:
            field_dict["subTasksEnabled"] = sub_tasks_enabled
        if issue_linking_enabled is not UNSET:
            field_dict["issueLinkingEnabled"] = issue_linking_enabled
        if time_tracking_enabled is not UNSET:
            field_dict["timeTrackingEnabled"] = time_tracking_enabled
        if attachments_enabled is not UNSET:
            field_dict["attachmentsEnabled"] = attachments_enabled
        if time_tracking_configuration is not UNSET:
            field_dict["timeTrackingConfiguration"] = time_tracking_configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        voting_enabled = d.pop("votingEnabled", UNSET)

        watching_enabled = d.pop("watchingEnabled", UNSET)

        unassigned_issues_allowed = d.pop("unassignedIssuesAllowed", UNSET)

        sub_tasks_enabled = d.pop("subTasksEnabled", UNSET)

        issue_linking_enabled = d.pop("issueLinkingEnabled", UNSET)

        time_tracking_enabled = d.pop("timeTrackingEnabled", UNSET)

        attachments_enabled = d.pop("attachmentsEnabled", UNSET)

        time_tracking_configuration: Union[Unset, TimeTrackingConfiguration] = UNSET
        _time_tracking_configuration = d.pop("timeTrackingConfiguration", UNSET)
        if not isinstance(_time_tracking_configuration, Unset):
            time_tracking_configuration = TimeTrackingConfiguration.from_dict(_time_tracking_configuration)

        configuration = cls(
            voting_enabled=voting_enabled,
            watching_enabled=watching_enabled,
            unassigned_issues_allowed=unassigned_issues_allowed,
            sub_tasks_enabled=sub_tasks_enabled,
            issue_linking_enabled=issue_linking_enabled,
            time_tracking_enabled=time_tracking_enabled,
            attachments_enabled=attachments_enabled,
            time_tracking_configuration=time_tracking_configuration,
        )

        return configuration
