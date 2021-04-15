import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.health_check_result import HealthCheckResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerInformation")


@attr.s(auto_attribs=True)
class ServerInformation:
    """ Details about the Jira instance. """

    base_url: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    version_numbers: Union[Unset, List[int]] = UNSET
    deployment_type: Union[Unset, str] = UNSET
    build_number: Union[Unset, int] = UNSET
    build_date: Union[Unset, datetime.datetime] = UNSET
    server_time: Union[Unset, datetime.datetime] = UNSET
    scm_info: Union[Unset, str] = UNSET
    server_title: Union[Unset, str] = UNSET
    health_checks: Union[Unset, List[HealthCheckResult]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url
        version = self.version
        version_numbers: Union[Unset, List[int]] = UNSET
        if not isinstance(self.version_numbers, Unset):
            version_numbers = self.version_numbers

        deployment_type = self.deployment_type
        build_number = self.build_number
        build_date: Union[Unset, str] = UNSET
        if not isinstance(self.build_date, Unset):
            build_date = self.build_date.isoformat()

        server_time: Union[Unset, str] = UNSET
        if not isinstance(self.server_time, Unset):
            server_time = self.server_time.isoformat()

        scm_info = self.scm_info
        server_title = self.server_title
        health_checks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.health_checks, Unset):
            health_checks = []
            for health_checks_item_data in self.health_checks:
                health_checks_item = health_checks_item_data.to_dict()

                health_checks.append(health_checks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if version is not UNSET:
            field_dict["version"] = version
        if version_numbers is not UNSET:
            field_dict["versionNumbers"] = version_numbers
        if deployment_type is not UNSET:
            field_dict["deploymentType"] = deployment_type
        if build_number is not UNSET:
            field_dict["buildNumber"] = build_number
        if build_date is not UNSET:
            field_dict["buildDate"] = build_date
        if server_time is not UNSET:
            field_dict["serverTime"] = server_time
        if scm_info is not UNSET:
            field_dict["scmInfo"] = scm_info
        if server_title is not UNSET:
            field_dict["serverTitle"] = server_title
        if health_checks is not UNSET:
            field_dict["healthChecks"] = health_checks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("baseUrl", UNSET)

        version = d.pop("version", UNSET)

        version_numbers = cast(List[int], d.pop("versionNumbers", UNSET))

        deployment_type = d.pop("deploymentType", UNSET)

        build_number = d.pop("buildNumber", UNSET)

        build_date: Union[Unset, datetime.datetime] = UNSET
        _build_date = d.pop("buildDate", UNSET)
        if not isinstance(_build_date, Unset):
            build_date = isoparse(_build_date)

        server_time: Union[Unset, datetime.datetime] = UNSET
        _server_time = d.pop("serverTime", UNSET)
        if not isinstance(_server_time, Unset):
            server_time = isoparse(_server_time)

        scm_info = d.pop("scmInfo", UNSET)

        server_title = d.pop("serverTitle", UNSET)

        health_checks = []
        _health_checks = d.pop("healthChecks", UNSET)
        for health_checks_item_data in _health_checks or []:
            health_checks_item = HealthCheckResult.from_dict(health_checks_item_data)

            health_checks.append(health_checks_item)

        server_information = cls(
            base_url=base_url,
            version=version,
            version_numbers=version_numbers,
            deployment_type=deployment_type,
            build_number=build_number,
            build_date=build_date,
            server_time=server_time,
            scm_info=scm_info,
            server_title=server_title,
            health_checks=health_checks,
        )

        return server_information
